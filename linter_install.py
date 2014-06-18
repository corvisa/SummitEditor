import sublime, sublime_plugin
import threading
import_error = False
try:
	package_manager = __import__("Package Control").package_control.package_manager
except ImportError:
	import_error = True

class LinterInstallCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		if import_error:
			sublime.error_message("Package Control is not installed. Install Package Control before continuing.")
			return
		t = threading.Thread(target=self.installer)
		t.start()

	def installer(self):
		pm = package_manager.PackageManager()
		pm.install_package('SublimeLinter')
		pm.install_package('SummitLinter')
		return

