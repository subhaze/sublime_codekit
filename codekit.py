import sublime, sublime_plugin, os, time

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


class CodeKit(Singleton):
    isST2 = int(sublime.version()) < 3000
    # Holds the property/values of the Sublime Text Settings file
    settings = None
    is_paused = False
    st_view_active = False
    # Used to ensure we're not making requests to CodeKit
    # on every view change in the same project
    folders_key = ''
    active_path = ''

    def run_apple_script(self, command):
        tell_code_kit = """osascript -e 'tell application "CodeKit" to %s'""" % command
        if self.isST2:
            os.system(tell_code_kit)
        else:
            sublime.set_timeout_async(
                lambda: os.system(tell_code_kit)
                , 0
            )

    # Handle auto activating CodeKit projects
    def activate_code_kit_project(self, view):
        # We're more than likely working with a view that's not been
        # saved yet, so bail since there's nothing we can do here.
        if not view.file_name():
            self.active_path = ''
            return

        abs_path = view.file_name()
        path, file_name = os.path.split(abs_path)
        # Check to see if the current file is within the same
        # path as a previous check, if so, assume project is active.
        # This helps reduce the amount of looping around dirs
        # looking for a config.codekit file
        if self.active_path and path.startswith(self.active_path):
            return
        # Reset the path to nothing since we're now looking for a new
        # codekit project file
        self.active_path = ''
        config_files = ['config.codekit', '.config.codekit3', 'config.codekit3']
        while path and not self.active_path:
            if [i for i in config_files if i in os.listdir(path)]:
                self.active_path = path
            path = '/'.join(path.split('/')[0:-1])

        if not self.settings.get('auto_switch_codekit_projects', True):
            return
        if self.active_path:
            sublime.active_window().run_command('codekit_select_project_from_view')

    # Handle CodeKit pause/unpause
    def handle_auto_pausing(self):
        if not self.settings.get('pause_codekit_on_view_deactivate', True):
            return
        if CodeKit().st_view_active and self.active_path:
            sublime.active_window().run_command('codekit_unpause')
        else:
            sublime.active_window().run_command('codekit_pause')

    def handle_view_activated(self, view):
        self.st_view_active = True
        self.activate_code_kit_project(view)
        self.handle_auto_pausing()

    def handle_view_deactivated(self, view):
        self.st_view_active = False

        # A bit of a hack due to ST triggering a deactivate then activate on the
        # same file when you open things like the command palette.
        # This should reduce a lot of false signaling to the CodeKit API
        def delayed_code_kit_pause():
            if not self.st_view_active:
                self.handle_auto_pausing()

        sublime.set_timeout(delayed_code_kit_pause, 144)


#
# Setup Settings file
#
def plugin_loaded():
    CodeKit().settings = sublime.load_settings('CodeKit.sublime-settings')

if CodeKit().isST2:
    plugin_loaded()
#
# End Setup Settings File
#


class CodekitEventListener(sublime_plugin.EventListener):
    import time
    def on_activated(self, view):
        if CodeKit().isST2:
            CodeKit().handle_view_activated(view)

    def on_activated_async(self, view):
        CodeKit().handle_view_activated(view)

    def on_deactivated(self, view):
        if CodeKit().isST2:
            CodeKit().handle_view_deactivated(view)

    def on_deactivated_async(self, view):
        CodeKit().handle_view_deactivated(view)

    def on_close(self, view):
       if len(sublime.windows()) < 1 and CodeKit().settings.get('auto_close_codekit', False):
        CodeKit().run_apple_script('quit')

#
# Add Project/Frame work commands
#
class CodekitAddProjectCommand(sublime_plugin.ApplicationCommand):
    folders = []

    def run(self, dirs=None, from_side_bar=False):
        if dirs and len(dirs) and from_side_bar:
            self.from_side_bar(dirs[0])
        elif not from_side_bar:
            self.from_command_palette()

    def get_project_folders(self):
        excludes = list(CodeKit().settings.get('exclude_dirs', []))
        folders = sublime.active_window().folders()
        paths = folders
        for root, dirs, files in os.walk(folders[0], topdown=True):
            dirs[:] = [root + '/' + d for d in dirs if d not in excludes]
            paths = paths + dirs
        return paths

    def from_command_palette(self):
        self.folders = self.get_project_folders()
        base_path = "/".join(self.folders[0].split('/')[:-1])
        sublime.active_window().show_quick_panel(
            [folder.replace(base_path, '')[1:] for folder in self.folders],
            self.on_done
        )

    def from_side_bar(self, folder):
        CodeKit().run_apple_script('add project at path "%s"' % folder)

    def on_done(self, indx):
        if indx > -1:
            CodeKit().run_apple_script('add project at path "%s"' % self.folders[indx])

    def is_enabled(self, dirs=None, from_side_bar=False):
        if dirs and len(dirs) or not from_side_bar:
            return True
        return False


class CodekitAddFrameworkCommand(sublime_plugin.ApplicationCommand):
    folders = []

    def run(self, dirs=None, from_side_bar=False):
        if dirs and len(dirs) and from_side_bar:
            self.from_side_bar(dirs[0])
        elif not from_side_bar:
            self.from_command_palette()

    def from_command_palette(self):
        self.folders = sublime.active_window().folders()
        sublime.active_window().show_quick_panel(
            [folder.split('/')[-1] for folder in self.folders],
            self.on_done
        )

    def from_side_bar(self, folder):
        CodeKit().run_apple_script('add framework at path "%s"' % folder)

    def on_done(self, indx):
        if indx > -1:
            CodeKit().run_apple_script('add framework at path "%s"' % self.folders[indx])

    def is_enabled(self, dirs=None, from_side_bar=False):
        if dirs and len(dirs) or not from_side_bar:
            return True
        return False


#
# Select Project/Framework commands
#
class CodekitSelectProjectFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        CodeKit().run_apple_script('select project containing path "%s"' % file_name)


class CodekitSelectFrameworkFromViewCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        file_name = sublime.active_window().active_view().file_name()
        CodeKit().run_apple_script('select framework containing path "%s"' % file_name)


#
# Pause/Unpause commands
# These commands only work IF auto-pausing is disabled
#
class CodekitPauseCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        if not CodeKit().is_paused:
            CodeKit().run_apple_script("pause file watching")
            CodeKit().is_paused = True

    def is_visible(self):
        return not CodeKit().settings.get('pause_codekit_on_view_deactivate')


class CodekitUnpauseCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        if CodeKit().is_paused:
            CodeKit().run_apple_script('unpause file watching')
            CodeKit().is_paused = False

    def is_visible(self):
        return not CodeKit().settings.get('pause_codekit_on_view_deactivate')


#
# Browser Commands
#
class CodekitPreviewInBrowserCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        CodeKit().run_apple_script('preview in browser')


class CodekitPreviewInBrowserSelectCommand(sublime_plugin.ApplicationCommand):

    browser_dict = {
        'Firefox': 'Firefox',
        'Firefox Developer Edition': 'bundle named "org.mozilla.firefoxdeveloperedition"',
        'Firefox Nightly': 'bundle named "org.mozilla.nightly"',
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
            CodeKit().run_apple_script('preview in browser %s' % self.browser_dict[key])


class CodekitRefreshBrowsersCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        CodeKit().run_apple_script('refresh browsers')


class CodekitReloadStyleSheetsCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        CodeKit().run_apple_script('refresh browsers by reloading just stylesheets')


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
