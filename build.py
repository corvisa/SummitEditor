import os
import platform
import sublime
import sublime_plugin

from subprocess import Popen

PACKAGES_PATH = sublime.packages_path()
INSTALLED_PACKAGES_PATH = sublime.packages_path()

if os.path.isdir('{0}/SummitEditor'.format(PACKAGES_PATH)):
    SUMMIT_PLUGIN_PATH = '{0}/SummitEditor'.format(PACKAGES_PATH)
elif os.path.isdir('{0}/SummitEditor'.format(INSTALLED_PACKAGES_PATH)):
    SUMMIT_PLUGIN_PATH = '{0}/SummitEditor'.format(INSTALLED_PACKAGES_PATH)
elif os.path.isdir('{0}/summiteditor'.format(INSTALLED_PACKAGES_PATH)):
    SUMMIT_PLUGIN_PATH = '{0}/summiteditor'.format(INSTALLED_PACKAGES_PATH)
elif os.path.isdir('{0}/summiteditor'.format(PACKAGES_PATH)):
    SUMMIT_PLUGIN_PATH = '{0}/summiteditor'.format(PACKAGES_PATH)


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

    def windows_build(self):
        pass

    def linux_build(self, opts=[]):
        cmd = ['bash', "{0}/simulate.sh".format(SUMMIT_PLUGIN_PATH), self.build_path]
        for opt in opts:
            cmd.append(opt)
        Popen(cmd)

    def darwin_build(self, opts=[]):
        cmd = ['bash', "{0}/simulate_mac.sh".format(SUMMIT_PLUGIN_PATH), self.build_path]
        for opt in opts:
            cmd.append(opt)
        print(cmd)
        Popen(cmd)


class SummitBuildWithArgs(SummitBuild):
    def _run(self, *args, **kwargs):
        self.window.show_input_panel("Simulator Arguments (--Arg Value):", "--DNIS", self.simulate_with_args, None, None)

    def simulate_with_args(self, sim_args):
        try:
            getattr(self, self.platform+'_build')(sim_args.split())
        except AttributeError:
            sublime.error_message(
                "Unable to determine operating system or platform '{0}' not supported.".format(self.platform))
