import sublime, sublime_plugin
import threading
try:
	package_manager = __import__("Package Control").package_control.package_manager
except ImportError:
	sublime.error_message("Package Control is not installed. Install Package Control before continuing.")

class LinterInstallCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		t = threading.Thread(target=self.installer)
		t.start()

	def installer(self):
		pm = package_manager.PackageManager()
		pm.install_package('SublimeLinter')
		pm.install_package('SummitLinter')
		return

