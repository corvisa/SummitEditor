import sublime
import sublime_plugin
import os
import re
import json

import_regex = """^(local\s+)?([\w\d_]+)\s*=\s*require\s*\(?['"]?(.+?)['"]?\)?$"""
object_regex = """^(?:local\s+)?([\w\d_]+)\s*=\s*([.\w\d_]*?)(?:\.initialize)?(?:\:(?:new|get))?(\(.*\))$"""

def is_summit_file(view):
    return view.match_selector(view.sel()[0].a, "source.lua.summit")

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
            plugin_folder = "SummitEditor"
            json_data = open(os.path.join(sublime.packages_path(), plugin_folder, source))
            self.completions = json.load(json_data)
            json_data.close()
    
    def replace_completions(self, c, module, import_map, object_map, trigger_or_contents, trigger_or_contents_list, comp_list):
        is_object = 'object' in c
        completion = trigger_or_contents
        completion_list = list(trigger_or_contents_list)
        if module is not None:
            if module in import_map and not is_object:
                import_name = import_map[module]
                import_depth = module.split('.')[-1]
                if ":" in completion.split('${')[0]:
                    old_caller = completion.split(':')[0]
                    if '.' in completion:
                        needed_depth = old_caller.split(import_depth)[-1]
                        new_caller =  import_name + needed_depth
                        completion = completion.replace(old_caller, new_caller, 1)
                    else:
                        completion = completion.replace(old_caller, import_name, 1)
                else:
                    covered_depth_part = completion.partition(import_depth)[:-1]
                    covered_depth = ''.join(covered_depth_part)
                    completion = completion.replace(covered_depth, import_name, 1)
            elif is_object:
                if len(object_map) < 1:
                    return "", []
                for import_name in object_map:
                    for obj_name in object_map[import_name]:
                        if object_map[import_name][obj_name] in module:
                            if ":" in completion.split('${')[0]:
                                old_caller = completion.split(':')[0]
                                completion_list.append(completion.replace(old_caller, obj_name, 1))
                            else:
                                old_caller = completion.split('.')[0]
                                completion_list.append(completion.replace(old_caller, obj_name, 1))
                        else:
                            for mod in comp_list:
                                if object_map[import_name][obj_name] in mod:
                                    valid_comp = True
                                    break
                                else:
                                    valid_comp = False
                            if not valid_comp:
                                return "", []
            else:   
                return "", []
        return completion, completion_list

    def find_completions(self, view, prefix, import_map, object_map):
        self.load_completions()
        completion_target = self.current_word(view)
        trim_result = completion_target.endswith(".")
        comps = []
        for c in self.completions['completions']:
            valid_comps = []
            if 'module' in c:
                if type(c['module']) is list:
                    valid_comps = list(c['module'])
                else:
                    valid_comps = list([c['module']])
            else:
                continue
            trigger = c['trigger']
            trigger_list = []
            contents = c['contents']
            contents_list = []
            for module in valid_comps:
                replaced_triggers = self.replace_completions(c, module, import_map, object_map, trigger, trigger_list, valid_comps)
                new_trigger, new_trigger_list = replaced_triggers[0], list(replaced_triggers[1])
                if not trim_result:
                    replaced_contents = self.replace_completions(c, module, import_map, object_map, contents, contents_list, valid_comps)
                    new_contents, new_contents_list = replaced_contents[0], list(replaced_contents[1])
                else:
                    new_contents = c['contents'].partition('.')[2]
                if new_trigger_list != []:
                    for i in range(len(new_trigger_list)):
                        try:
                            comps.append((new_trigger_list[i], new_contents_list[i])) 
                        except IndexError:
                            pass
                elif trigger is not "":
                    comps.append((new_trigger, new_contents))
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
            module = pair.split(',')[1]
            import_name = pair.split(',')[0]
            import_map[module] = import_name
            for obj in object_extractions:
                obj_depth = obj.split(',')[1]
                obj_creator = obj_depth.split('.')[0]
                obj_name = obj.split(',')[0]
                if obj_creator == import_name:
                    callee = obj.split(',')[1]
                    depth_num = len(callee.split('.'))
                    if depth_num < 2:
                        obj_type = module.split('.')[-1]
                    else:
                        obj_type = callee.split('.')[1]
                    if obj_creator not in object_map:
                        object_map[obj_creator] = {obj_name: obj_type}
                    else:
                        object_map[obj_creator][obj_name] = obj_type
                else:
                    for obj in object_map:
                        if obj_creator in object_map[obj]:
                            if len(obj_depth.split('.')) > 1: 
                                object_map[obj][obj_name] = '.'.join([object_map[obj][obj_creator], '.'.join(obj_depth.split('.')[1:])])
                            else:
                                object_map[obj][obj_name] = object_map[obj][obj_creator]
                            break
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