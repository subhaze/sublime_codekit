#[CodeKit](https://incident57.com/codekit/) 2 plug-in for Sublime Text

##Current CodeKit features
- Automatically switch CodeKit project based on current view
- - You can disable this in the settings
- Pause/Unpause CodeKit based on Sublime Text focus
- - __Todo:__ Add Pause/Unpause to Command Palette
- - __Todo:__ Add setting to disable auto pause/unpause based on Sublime Text focus
- Add folder from Sublime Text's sidebar as a CodeKit project
- Add folder from Sublime Text's sidebar as a CodeKit framework
- Select a project in CodeKit base on the active view
- Select a framework in CodeKit base on the active view
- Preview in browser
- Preview in selected browser from list
- Refresh browser
- Reload style sheets

----

##Installation

You'll need [Package Control](https://sublime.wbond.net/installation) installed. Once you've got that setup all you have to do is open the Command Palette (super+shift+p) then type `install package` hit enter, then search for 'CodeKit Commands' and select it.

----

##How it works

###Auto-active CodeKit projects
When you open a project in Sublime Text, CodeKit will automatically open for you (if it's not already open) and then set the active project in CodeKit based on the project you're working on. If you have a few different projects open, this plug-in will automatically change what project is active in CodeKit based on what file you're currently editing.

###Manually activate CodeKit projects
You can disable auto-project switching by disabling `Preferences>Package Settings>CodeKit Commands>Enable Auto Switch CodeKit Project` and you can still change the active project in CodeKit from Sublime via the Command Palette commands `CodeKit Select project` or `CodeKit Select framework`.

###Adding projects to CodeKit
If you're currently working on a project or framework that CodeKit doesn't know about, simply fire up the Command Palette and run the command `CodeKit Add project` or `CodeKit Add framework`. You'll be presented with a list of folders specific to your current Sublime project to select from and add to CodeKit.

###Auto-pausing CodeKit
By default this plug-in will pause CodeKit when you're not focused on Sublime Text. This can be useful if you use the CLI or third-party tools to handle source control.

CodeKit states:
>Before you perform any action that will change large numbers of files at once (switching branches, rebasing, pull requests, etc.) you MUST tell CodeKit to ignore file changes.

If you'd rather handle toggling the paused state of CodeKit manually you can disable this feature via `Preferences>Package Settings>CodeKit Commands>Enable Auto Pausing` and run the `CodeKit pause` and `CodeKit unpause` commands from the Command Palette. __Heads Up__ These two commands do nothing if you have auto-pausing enabled (which it is by default).

More details about why it can be good to pause and other critical things to know about CodeKit can be found [here](http://incident57.com/codekit/help.html#critical-things).

###Handling browsers
You also have access to browser refreshing, style sheet reloading, browser specific previewing all from the Command Palette. Just type `CodeKit` to see the full list. Any new commands added to Command Palette will always be prefixed with `CodeKit` for easy viewing/access.