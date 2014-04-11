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

        self._run()

    def _run(self):
        try:
            getattr(self, self.platform+'_build')()
        except AttributeError:
            sublime.error_message(
                "Unable to determine operating system or platform '{0}' not supported.".format(self.platform))

    def windows_build(self, opts=[]):
        cmd = [
            'bash.exe',
            "{0}\simulate_windows.sh".format(SUMMIT_PLUGIN_PATH),
            self.build_path,
            SUMMIT_SETTINGS.get("summit_simulator_host")
        ]
        for opt in opts:
            cmd.append(opt)
        Popen(cmd)

    def linux_build(self, opts=[]):
        cmd = [
            'bash',
            "{0}/simulate.sh".format(SUMMIT_PLUGIN_PATH),
            self.build_path,
            SUMMIT_SETTINGS.get("summit_simulator_host")
        ]

        for opt in opts:
            cmd.append(opt)
        Popen(cmd)

    def darwin_build(self, opts=[]):
        cmd = [
            'bash',
            "{0}/simulate_mac.sh".format(SUMMIT_PLUGIN_PATH),
            self.build_path,
            SUMMIT_SETTINGS.get("summit_simulator_host"),
        ]
        for opt in opts:
            cmd.append(opt)
        Popen(cmd)


class SummitBuildWithArgs(SummitBuild):
    def _run(self, *args, **kwargs):
        self.window.show_input_panel("Simulator Arguments (--Arg Value):", "--DNIS ", self.simulate_with_args, None, None)

    def simulate_with_args(self, sim_args):
        try:
            getattr(self, self.platform+'_build')(sim_args.split())
        except AttributeError:
            sublime.error_message(
                "Unable to determine operating system or platform '{0}' not supported.".format(self.platform))
