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


class SummitBuild(sublime_plugin.WindowCommand):

    def run(self):
        try:
            self.build_path = self.window.project_data()['build_path']
        except KeyError:
            sublime.error_message('Unable to find required project setting "build_path"')

        self.plat = platform.system()

        if self.plat == "Windows":
            self.run_windows()
        elif self.plat == "Linux":
            self.run_linux()
        elif self.plat == "Darwin":
            self.run_mac()
        else:
            sublime.error_message(
                "Unable to determine operating system. {0} not supported.".format(self.plat))

    def run_linux(self):
        self.linux_build()

    def run_windows(self):
        pass

    def run_mac(self):
        pass

    def linux_build(self, opts=[]):
        cmd = ['/bin/bash', "{0}/simulate.sh".format(SUMMIT_PLUGIN_PATH), self.build_path]
        for opt in opts:
            cmd.append(opt)

        print(cmd)
        Popen(cmd)


class SummitBuildWithArgs(SummitBuild):
    def run_linux(self, *args, **kwargs):
        self.window.show_input_panel("Simulator Arguments (--Arg Value):", "--DNIS", self.simulate_with_args, None, None)

    def simulate_with_args(self, sim_args):
        self.linux_build(sim_args.split())
