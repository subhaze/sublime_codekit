import sublime, sublime_plugin, os

#
# Helper Utils
#
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


Singleton = _Singleton('SingletonMeta', (object,), {})
#
# Ends Helper Utils
#


class CodeKitState(Singleton):
    isST2 = int(sublime.version()) < 3000
    # Holds the property/values of the Sublime Text Settings file
    settings = None
    # Used to know if CodeKit should be paused/unpaused
    is_active = False
    # Used to ensure we're not making requests to CodeKit
    # on every view change in the same project
    folders_key = ''

    # Handle CodeKit pause/unpause
    def handle_pausing(self, active=False):
        if not self.settings.get('pause_codekit_on_view_deactivate', True):
            return
        if active: self.unpause_code_kit()
        else: self.pause_code_kit()

    def unpause_code_kit(self):
        # If we don't see Sublime Text as active, make it so
        # and unpause CodeKit
        if not CodeKitState().is_active:
            os.system("""osascript -e 'tell application "CodeKit" to unpause file watching'""")
            CodeKitState().is_active = True

    def pause_code_kit(self):
        print('pause codekit')
        if not CodeKitState().is_active:
            os.system("""osascript -e 'tell application "CodeKit" to pause file watching'""")
            CodeKitState().is_active = False

    # Handle auto activating CodeKit projects
    def active_code_kit_project(self):
        if not self.settings.get('auto_switch_codekit_projects', True):
            return

        current_folders_key = '-'.join(sublime.active_window().folders())
        if current_folders_key != self.folders_key:
            self.folders_key = current_folders_key
            sublime.active_window().run_command('codekit_select_project_from_view')


if CodeKitState().isST2:
    CodeKitState().settings = sublime.load_settings('CodeKit.sublime-settings')


def plugin_loaded():
    CodeKitState().settings = sublime.load_settings('CodeKit.sublime-settings')


class CodekitEventListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        CodeKitState().handle_pausing(active=True)
        CodeKitState().active_code_kit_project()

    def on_deactivated(self, view):
        CodeKitState().is_active = False
        sublime.set_timeout(CodeKitState().handle_pausing, 10)


#
# Add Project/Frame work commands
#
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


#
# Select Project/Framework commands
#
class CodekitSelectProjectFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        os.system("""osascript -e 'tell application "CodeKit" to select project containing path "%s"'""" % file_name)


class CodekitSelectFrameworkFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        os.system("""osascript -e 'tell application "CodeKit" to select framework containing path "%s"'""" % file_name)


#
# Pause/Unpause commands
# These commands only work IF auto-pausing is disabled
#
class CodekitPauseCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        CodeKitState().pause_code_kit()


class CodekitUnpauseCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        CodeKitState().unpause_code_kit()


#
# Browser Commands
#
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


#
# Settings Helpers
#
class CodekitToggleSettingsCommand(sublime_plugin.ApplicationCommand):

    """Enables/Disables settings"""

    def run(self, setting):
        s = sublime.load_settings('CodeKit.sublime-settings')
        s.set(setting, not s.get(setting, False))
        sublime.save_settings('CodeKit.sublime-settings')

    def is_checked(self, setting):
        s = sublime.load_settings('CodeKit.sublime-settings')
        return s.get(setting, False)
