"""
    The MIT License (MIT)

    Copyright (c) 2014 CorvisaCloud, LLC

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import os
import platform
import sublime
import sublime_plugin

from subprocess import Popen

SUMMIT_PLUGIN_PATH = os.path.split(os.path.abspath(__file__))[0]


class SummitBuild(sublime_plugin.WindowCommand):
    def run(self):
        self.SUMMIT_SETTINGS = sublime.load_settings('SummitEditor.sublime-settings')
        try:
            self.build_path = self.window.project_data()['build_path']
        except KeyError:
            sublime.error_message('Unable to find required project setting "build_path"')
        self.platform = platform.system().lower()

        self.build()

    def build(self, opts=[]):
        if self.platform not in ['windows', 'darwin', 'linux']:
            sublime.error_message(
                "Unable to determine operating system or platform '{0}' not supported.".format(self.platform))
            return

        cmd = [
            'bash',
            "{}{}simulate_{}.sh".format(SUMMIT_PLUGIN_PATH, os.path.sep, self.platform),
            self.build_path,
            self.SUMMIT_SETTINGS.get("summit_simulator_host", "code.corvisacloud.com"),
            self.SUMMIT_SETTINGS.get("summit_simulator_user", "debug")
        ]

        #If there is an app id specified in the project settings, pass it to the simulator
        try:
            app_id = self.window.project_data()['application_id']
            opts.append(app_id)
        except KeyError:
            pass

        for opt in opts:
            cmd.append(opt)

        Popen(cmd)


class SummitBuildWithArgs(SummitBuild):
    def run(self, *args, **kwargs):
        try:
            self.build_path = self.window.project_data()['build_path']
        except KeyError:
            sublime.error_message('Unable to find required project setting "build_path"')
        self.platform = platform.system().lower()

        self.window.show_input_panel("Simulator Arguments (--Arg Value):", "--DNIS ", self.simulate_with_args, None, None)

    def simulate_with_args(self, sim_args):
        self.build(sim_args.split())


class SummitAutoBuildOnSave(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        self.SUMMIT_SETTINGS = sublime.load_settings('SummitEditor.sublime-settings')

        super(SummitAutoBuildOnSave, self).__init__(*args, **kwargs)

    def on_post_save(self, view):
        is_summit_file = view.scope_name(0).startswith('source.lua.summit')
        auto_build = self.SUMMIT_SETTINGS.get('summit_simulate_on_save', False)

        if is_summit_file and auto_build:
            sublime.active_window().run_command('build')
