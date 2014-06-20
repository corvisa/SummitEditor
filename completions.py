import sublime
import sublime_plugin
import os
import re
import json

import_regex = """^(local\s+)?([\w\d_]+)\s*=\s*require\s*\(?['"]?(.+?)['"]?\)?$"""

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

    def find_completions(self, view, prefix, import_map):
        self.load_completions()
        completion_target = self.current_word(view)
        trim_result = completion_target.endswith(".")

        comps = []
        for c in self.completions['completions']:
            trigger = ""
            contents = ""
            # if isinstance(c, dict):
            if 'module' in c:
                if c['module'] not in import_map:
                    if c['module'] is not None:
                        continue
            else:
                continue
            trigger = c['trigger']
            if c['module'] is not None:
                trigger = trigger.replace(c['trigger'].split('.')[0], import_map[c['module']], 1)
            if not trim_result:
                contents = c['contents']
                if c['module'] is not None:
                    contents = contents.replace(contents.split('.')[0], import_map[c['module']], 1)
            else:
                contents = c['contents'].partition('.')[2]
            # elif is_string_instance(c):
            #     if self.fuzzyMatchString(c, use_fuzzy_completion):
            #         trigger = c
            #         contents = c

            if trigger is not "":
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
            view.settings().set("word_separators", self.default_separators.replace('.', ''))

    def on_query_completions(self, view, prefix, locations):
        import_map = {}
        extractions = []
        view.find_all(import_regex, 0, r'\2,\3', extractions)
        for pair in extractions:
            import_map[pair.split(',')[1]] = pair.split(',')[0]
        use_summit_editor_completion = True
        if use_summit_editor_completion and view.match_selector(locations[0], "source.lua.summit - entity"):
            comps = self.find_completions(view, prefix, import_map)
            flags = 0
            return (comps, flags)
        else:
            return []

    def on_modified(self, view):
        if not self.correct_syntax and is_summit_file(view):
            self.correct_syntax = True
            self.on_load(view)