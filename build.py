import os
import platform
import sublime
import sublime_plugin

from subprocess import Popen

SUMMIT_PLUGIN_PATH = os.path.split(os.path.abspath(__file__))[0]
SUMMIT_SETTINGS = sublime.load_settings('SummitEditor.sublime-settings')


class SummitBuild(sublime_plugin.WindowCommand):

    def run(self):
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
            SUMMIT_SETTINGS.get("summit_simulator_host")
        ]
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
