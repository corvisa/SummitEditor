import sublime
import sublime_plugin
import os
import re
import json

import_regex = """^(local\s+)?([\w\d_]+)\s*=\s*require\s*\(?['"]?(.+?)['"]?\)?$"""
object_regex = """^(?:local\s+)?([\w\d_]+)\s*=\s*([.\w\d_]*?)(?:\.initialize)?(?:\:new)?(\(.*\))$"""

def is_summit_file(view):
    return view.match_selector(view.sel()[0].a, "source.lua.summit")

# def is_string_instance(obj):
#     try:
#         return isinstance(obj, basestring)
#     except NameError:
#         return isinstance(obj, str)

def get_setting(setting):
    settings = sublime.load_settings("SummitEditor.sublime-settings")
    return settings.get(setting)

class SummitCompletions:
    completions = []

    def __init__(self):
        self.load_completions()

    def load_completions(self):
        if len(self.completions) == 0:
            source = get_setting("completions_file")
            plugin_folder = "summiteditor"
            json_data = open(os.path.join(sublime.packages_path(), plugin_folder, source))
            self.completions = json.load(json_data)
            json_data.close()

    def find_completions(self, view, prefix, import_map, object_map):
        self.load_completions()
        completion_target = self.current_word(view)
        trim_result = completion_target.endswith(".")

        comps = []
        for c in self.completions['completions']:
            trigger = ""
            contents = ""
            valid_comps = []
            # if isinstance(c, dict):
            if 'module' in c:
                if type(c['module']) is list:
                    comp_list = list(c['module'])
                else:
                    comp_list = list([c['module']])
                for module in comp_list:
                    if module not in import_map:
                        if module is not None:
                            continue
                    else:
                        valid_comps.append(module)           
            else:
                continue
            if "no_replace" in c:
                continue
            trigger = c['trigger']
            trigger_list = []
            contents_list = []
            for module in valid_comps:
                if module is not None:
                    if 'object' not in c:
                        if ":" in trigger:
                            if '.' in trigger:
                                trigger = trigger.replace(c['trigger'].split(':')[0], import_map[module] + c['trigger'].split(':')[0].split(module.split('.')[-1])[-1], 1)
                            else:
                                trigger = trigger.replace(c['trigger'].split(':')[0], import_map[module], 1)
                        else:    
                            trigger = trigger.replace(''.join(c['trigger'].partition(module.split('.')[-1])[:-1]), import_map[module], 1)
                    elif import_map[module] in object_map:
                        for obj in object_map[import_map[module]]:
                            if ":" in trigger:
                                if object_map[import_map[module]][obj] in trigger.split(':')[0]:
                                    trigger_list.append(trigger.replace(c['trigger'].split(':')[0], obj, 1))
                            else:
                                trigger_list.append(trigger.replace(c['trigger'].split('.')[0], obj, 1))


                if not trim_result:
                    contents = c['contents']
                    if module is not None:
                        if 'object' not in c:
                            if ":" in c['trigger']:
                                if '.' in c['trigger']:
                                    contents = contents.replace(c['contents'].split(':')[0], import_map[module] + c['contents'].split(':')[0].split(module.split('.')[-1])[-1], 1)
                                else:
                                    contents = contents.replace(c['contents'].split(':')[0], import_map[module], 1)
                            else:
                                contents = contents.replace(''.join(c['contents'].partition(module.split('.')[-1])[:-1]), import_map[module], 1)
                        elif import_map[module] in object_map:
                            for obj in object_map[import_map[module]]:
                                if ":" in trigger:
                                    if object_map[import_map[module]][obj] in trigger.split(':')[0]:
                                        contents_list.append(contents.replace(c['contents'].split(':')[0], obj, 1))
                                else:
                                    contents_list.append(contents.replace(c['contents'].split('.')[0], obj, 1))
                else:
                    contents = c['contents'].partition('.')[2]
                # elif is_string_instance(c):
                #     if self.fuzzyMatchString(c, use_fuzzy_completion):
                #         trigger = c
                #         contents = c
                if trigger_list != []:
                    for i in range(len(trigger_list)):
                        try:
                            comps.append((trigger_list[i], contents_list[i])) 
                        except IndexError:
                            pass
                elif trigger is not "":
                    comps.append((trigger, contents))

        for c in view.extract_completions(completion_target):
            comps.append((c, c))

        comps = list(set(comps))
        comps.sort()
        return comps

    def current_word(self, view):
        s = view.word(view.sel()[0])
        return view.substr(s)

class CompletionsListener(SummitCompletions, sublime_plugin.EventListener):

    def __init__(self):
        self.periods_set = {}
        self.default_separators = ''
        self.correct_syntax = False

    def on_load(self, view):
        use_summit_editor_completion = get_setting('use_summit_editor_completion')
        if use_summit_editor_completion and is_summit_file(view):
            self.correct_syntax = True
            self.default_separators = view.settings().get("word_separators")
            remove_periods = self.default_separators.replace('.', '')
            view.settings().set("word_separators", remove_periods.replace(':', ''))

    def on_query_completions(self, view, prefix, locations):
        import_map = {}
        object_map = {}
        import_extractions = []
        object_extractions = []
        view.find_all(import_regex, 0, r'\2,\3', import_extractions)
        view.find_all(object_regex, 0, r'\1,\2', object_extractions)
        for pair in import_extractions:
            import_map[pair.split(',')[1]] = pair.split(',')[0]
            for obj in object_extractions:
                if obj.split(',')[1].split('.')[0] == pair.split(',')[0]:
                    if len(obj.split(',')[1].split('.')) < 2:
                        lastModule = pair.split(',')[1].split('.')[-1]
                    else:
                        lastModule = obj.split(',')[1].split('.')[1]
                    if obj.split(',')[1].split('.')[0] not in object_map:
                        
                            object_map[obj.split(',')[1].split('.')[0]] = {obj.split(',')[0]: lastModule}
                    else:
                        object_map[obj.split(',')[1].split('.')[0]][obj.split(',')[0]] = lastModule
        use_summit_editor_completion = get_setting('use_summit_editor_completion')
        if use_summit_editor_completion and view.match_selector(locations[0], "source.lua.summit - entity"):
            comps = self.find_completions(view, prefix, import_map, object_map)
            flags = 0
            return (comps, flags)
        else:
            return []

    def on_modified(self, view):
        if not self.correct_syntax and is_summit_file(view):
            self.correct_syntax = True
            self.on_load(view)