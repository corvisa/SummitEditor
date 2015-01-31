import sublime
import sublime_plugin
import os
import re
import json

import_regex = r"""^(local\s+)?([\w\d_]+)\s*=\s*require\s*\(?['"]?(.+?)['"]?\)?$"""

# assign_regex matches multiple types of lua assignments
# examples:
#
# local setrow = chain:insert(value) -- with an ending comment
# setrow = chain:insert(value) -- with an ending comment
# local db = datastore.get_table(name, type)
# db = datastore.get_table(name, type)
# somevar = tbl.some_field
# somevar = tbl.some_field -- with a comment
assign_regex = r"""^[ \t]*(?:local\s+)?([\w\d_.,]+)\s*=\s*([\w\d_.:]+)\s*(?:\(.*\)\s*)?(?:--.*)?$"""


def is_summit_file(view):
    return view.match_selector(view.sel()[0].a, "source.lua.summit")


def get_setting(setting):
    settings = sublime.load_settings("SummitEditor.sublime-settings")
    return settings.get(setting)


def within_require(line):
    req_match = re.match(
        r"""^((?:local\s+)?(?:[\w\d_]+)\s*=\s*require\s*\(?['"]?)""",
        line[0])
    if req_match is not None:
        if len(req_match.group(1)) <= line[1]:
            return True

    return False


class SummitCompletions:
    completions = []
    obj_types = {}

    def __init__(self):
        self.completions = []
        self.obj_types = {}
        self.load_completions()

    def load_completions(self):
        if len(self.completions) == 0:
            source = get_setting("completions_file")
            plugin_folder = "SummitEditor"
            json_data = open(os.path.join(sublime.packages_path(),
                                          plugin_folder,
                                          source))
            self.completions = json.load(json_data)
            json_data.close()

            # After loading, go through all the objects
            # and create a single lookup table for them so
            # it's faster to find them when completing object type
            # queries
            for mod_name in self.completions['modules']:
                module = self.completions['modules'][mod_name]
                if not 'objects' in module:
                    continue

                for obj in module['objects']:
                    self.obj_types[obj] = module['objects'][obj]

    def default_imports(self):
        self.load_completions()

        return self.completions['imports']

    def find_return_types(self, symbol, imports, objects):
        """
        Attempts to find the return types for the given symbol.

        Returns either a list of types for each return value
        or None if not found.
        """

        if symbol is None or imports is None or len(imports) == 0:
            return None

        self.load_completions()

        self_parts = symbol.split(':')
        sym_parts = self_parts[0].split('.')
        obj_name = '.'.join(sym_parts[:1])
        target_name = '.' + sym_parts[-1]

        if len(self_parts) > 1:
            # If there's something on the right side
            # of a self call, use that as the target
            target_name = ':' + self_parts[-1]

        if obj_name not in imports:
            # If the object isn't an import, it could be the
            # result of another method call. See if it's in the
            # objects instead
            if obj_name in objects:
                found_types = objects[obj_name]

                if len(sym_parts) == 1 and len(self_parts) == 1:
                    # If there's only one part to the symbols and
                    # it's an object name, treat it as a __call (stored
                    # in the data as an empty function)
                    target_name = ''

                rhs_types = []
                for found_type in found_types:
                    # found_types are the potential types that obj_name
                    # can be, so iterate over them and try to get the
                    # function and field data for each of those types
                    type_opts = self.obj_types.get(found_type)
                    if type_opts:
                        # found the type we were looking for, so see if we find
                        # a match for the target (such as a function call) and
                        # then add the return values for that function/field
                        # to the correct set of returns
                        type_funcs = type_opts['functions']
                        if target_name in type_funcs:
                            returns = type_funcs[target_name].get('returns')
                            if returns:
                                ret_types_diff = len(returns) - len(rhs_types)
                                for _ in range(0, ret_types_diff):
                                    # Add any missing return sets to the list
                                    rhs_types.append(set())

                                for type_idx, ret_types in enumerate(returns):
                                    ret_idx_types = rhs_types[type_idx]
                                    for ret_type in ret_types:
                                        ret_idx_types.add(ret_type)

                        type_fields = type_opts['fields']
                        if target_name in type_fields:
                            returns = type_fields[target_name].get('returns')
                            if returns:
                                ret_types_diff = len(returns) - len(rhs_types)
                                for _ in range(0, ret_types_diff):
                                    # Add any missing return sets to the list
                                    rhs_types.append(set())

                                for type_idx, ret_types in enumerate(returns):
                                    ret_idx_types = rhs_types[type_idx]
                                    for ret_type in ret_types:
                                        ret_idx_types.add(ret_type)

                return rhs_types

            return None

        module_name = imports[obj_name]

        if module_name not in self.completions['modules']:
            return None

        module = self.completions['modules'][module_name]

        if target_name in module['fields']:
            return module['fields'][target_name]['returns']

        if target_name in module['functions']:
            return module['functions'][target_name]['returns']

        return None

    def find_completions(self, view, prefix, imports, objects):
        completion_target = self.current_word(view)
        if completion_target.endswith('.') or completion_target.endswith(':'):
            completion_target = completion_target[:-1]

        self.load_completions()

        comps = []
        used_names = set()

        modules = self.completions['modules'] or []

        current_line = self.current_line(view)
        if within_require(current_line):
            # If within a require, add all the known modules
            # to help out the user
            for mod_name in modules.keys():
                comps.append((mod_name, mod_name))

        valid_modules = []
        for imp in imports:
            if not imp.startswith(completion_target):
                continue

            valid_modules.append((imp, imports[imp]))

        for module in valid_modules:
            imp_name = module[0]
            mod_name = module[1]

            if mod_name not in modules:
                continue

            mod_doc = modules[mod_name]
            for fn_name in mod_doc['functions']:
                func = mod_doc['functions'][fn_name]
                comps.append(
                    (imp_name+func['trigger'], imp_name+func['contents'])
                )
            for f_name in mod_doc['fields']:
                field = mod_doc['fields'][f_name]
                comps.append(
                    (imp_name+field['trigger'], imp_name+field['contents'])
                )

        for obj in objects:
            if not obj.startswith(completion_target):
                continue

            obj_types = [item for item in objects[obj] if item != 'nil']
            for t in obj_types:
                # Go through all the known objects to see
                # if they're a match for this return type
                if not t in self.obj_types:
                    continue

                obj_symbols = self.obj_types[t]
                for fn_name in obj_symbols['functions']:
                    func = obj_symbols['functions'][fn_name]
                    used_names.add(obj+fn_name)
                    comps.append(
                        (obj+func['trigger'], obj+func['contents'])
                    )
                for f_name in obj_symbols['fields']:
                    field = obj_symbols['fields'][f_name]
                    comps.append(
                        (obj+field['trigger'], obj+field['contents'])
                    )

        for c in view.extract_completions(completion_target):
            # Don't include any completions that end with . because
            # it looks weird and ends up with duplicates like:
            # mymenu
            # mymenu.
            if re.search(r'[\.:]$', c) is None and c not in used_names:
                comps.append((c, c))

        comps.sort()
        comps = list(set(comps))
        return comps

    def current_line(self, view):
        first_sel = view.sel()[0]
        s = view.line(first_sel)
        line_pos = (s.b-s.a)-(s.b - first_sel.b)
        return view.substr(s), line_pos

    def current_word(self, view):
        s = view.word(view.sel()[0])
        return view.substr(s)


class CompletionsListener(SummitCompletions, sublime_plugin.EventListener):
    def __init__(self):
        # Don't do super().__init__() or even try to do
        # SummitCompletions.__init__(self) here because apparently it causes
        # Sublime to not hook the event methods...?

        self.periods_set = {}
        self.default_separators = ''
        self.correct_syntax = False

    def on_load(self, view):
        use_completion = get_setting('use_summit_editor_completion')
        if use_completion and is_summit_file(view):
            self.correct_syntax = True
            self.default_separators = view.settings().get("word_separators")
            remove_periods = self.default_separators.replace('.', '')
            view.settings().set("word_separators",
                                remove_periods.replace(':', ''))

    def on_query_completions(self, view, prefix, locations):
        use_completion = get_setting('use_summit_editor_completion')
        if not use_completion:
            return []

        imports = dict(super().default_imports()) or {}
        objects = {}

        import_extractions = []
        fn_extractions = []
        view.find_all(import_regex, 0, r'\2,\3', import_extractions)
        view.find_all(assign_regex, 0, r'\1|\2', fn_extractions)

        for pair in import_extractions:
            import_name = pair.split(',')[0]
            module = re.sub(r'(\'|")', '', pair.split(',')[1])

            imports[import_name] = module

        for pair in fn_extractions:
            assigns = pair.split('|')
            if len(assigns) != 2:
                continue

            lhs = [item.strip() for item in assigns[0].split(',')]
            rhs = assigns[1]

            rhs_types = super().find_return_types(rhs, imports, objects)

            if rhs_types:
                # Only bother enumerating if we know the rhs
                for lhs_part in enumerate(lhs):
                    obj_name = lhs_part[1]
                    obj_types = rhs_types[lhs_part[0]]

                    if obj_name not in objects:
                        # We haven't seen this name before, add it
                        # to the known objects
                        objects[obj_name] = set(obj_types)
                    else:
                        cur_obj_types = objects[obj_name]
                        for obj_type in obj_types:
                            if obj_type not in cur_obj_types:
                                cur_obj_types.add(obj_type)

        if view.match_selector(locations[0], "source.lua.summit - entity"):
            comps = self.find_completions(view, prefix, imports, objects)
            flags = 0
            return (comps, flags)
        else:
            return []

    def on_modified(self, view):
        if not self.correct_syntax and is_summit_file(view):
            self.correct_syntax = True
            self.on_load(view)
