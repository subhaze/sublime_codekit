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


class CodekitAddFrameworkCommand(sublime_plugin.ApplicationCommand):
    folders = []

    def run(self):
        self.folders = sublime.active_window().folders()
        sublime.active_window().show_quick_panel(
            [folder.split('/')[-1] for folder in self.folders],
            self.on_done
        )

    def on_done(self, indx):
        if indx > -1:
            os.system("""osascript -e 'tell application "CodeKit" to add framework at path "%s"'""" % self.folders[indx])


class CodekitSelectProjectFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        os.system("""osascript -e 'tell application "CodeKit" to select project containing path "%s"'""" % file_name)


class CodekitSelectFrameworkFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        os.system("""osascript -e 'tell application "CodeKit" to select framework containing path "%s"'""" % file_name)


class CodekitPreviewInBrowserCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to preview in browser'""")


class CodekitPreviewInBrowserSelectCommand(sublime_plugin.ApplicationCommand):

    browser_dict = {
        'Firefox': 'Firefox',
        'FireFoxNightly': 'bundle named "org.mozilla.nightly"',
        'Chrome': 'Chrome',
        'Chrome Canary': 'Chrome Canary',
        'Chromium': 'Chromium',
        'Opera': 'Opera',
        'Opera Developer': 'bundle named "com.operasoftware.OperaDeveloper"',
        'Opera Next': 'bundle named "com.operasoftware.OperaNext"',
        'Safari': 'Safari',
        'Webkit Nightly': 'Webkit Nightly'
    }

    browser_keys = sorted(list(browser_dict.keys()))

    def run(self):
        sublime.active_window().show_quick_panel(
            self.browser_keys,
            self.on_done
        )

    def on_done(self, indx):
        if indx > -1:
            key = self.browser_keys[indx]
            os.system("""osascript -e 'tell application "CodeKit" to preview in browser %s'""" % self.browser_dict[key])


class CodekitRefreshBrowsersCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to refresh browsers'""")


class CodekitReloadStyleSheetsCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        os.system("""osascript -e 'tell application "CodeKit" to refresh browsers by reloading just stylesheets'""")