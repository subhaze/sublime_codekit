import sublime, sublime_plugin, os


class CodekitEventListener(sublime_plugin.EventListener):
    is_active = False

    def on_activated(self, view):
        if not self.is_active:
            os.system("""osascript -e 'tell application "CodeKit" to unpause file watching'""")
            self.is_active = True

    def on_deactivated(self, view):
        self.is_active = False
        sublime.set_timeout(self.pause_code_kit, 10)

    def pause_code_kit(self):
        if not self.is_active:
            os.system("""osascript -e 'tell application "CodeKit" to pause file watching'""")


class CodekitAddProjectCommand(sublime_plugin.ApplicationCommand):
    folders = []

    def run(self):
        self.folders = sublime.active_window().folders()
        sublime.active_window().show_quick_panel(
            [folder.split('/')[-1] for folder in self.folders],
            self.on_done
        )

    def on_done(self, indx):
        if indx > -1:
            os.system("""osascript -e 'tell application "CodeKit" to add project at path "%s"'""" % self.folders[indx])


class CodekitSelectProjectFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        os.system("""osascript -e 'tell application "CodeKit" to select project containing path "%s"'""" % file_name)


class CodekitPreviewInBrowserCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to preview in browser'""")


class CodekitRefreshBrowsersCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to refresh browsers'""")


class CodekitReloadStyleSheetsCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to refresh browsers by reloading just stylesheets'""")