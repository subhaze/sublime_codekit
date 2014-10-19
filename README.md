#[CodeKit](https://incident57.com/codekit/) 2 plug-in for Sublime Text


##Installation

*[CodeKit Commands](https://sublime.wbond.net/packages/CodeKit%20Commands)* should be installed via [Package Control](https://sublime.wbond.net/installation).

----

##How it works

###Auto-active CodeKit projects
When you open a project in Sublime Text, CodeKit will automatically open for you, if it's not already open, and then set the active project in CodeKit based on the current file you're working on. So if you have a few different projects open, even files in different projects but in the same window, this plug-in will keep CodeKit focused on the project you're focused on so you don't have to.

Auto-activate will look for a `config.codekit` file in the active file's directory or walk up the directory tree until it either finds a `config.codekit` file and sends a signal to CodeKit or reaches the OS root directory and does nothing. Some path caching is done to prevent lots of unnecessary directory walks when
you're switching between files in the same directory tree.

###Manually activate CodeKit projects
You can disable auto-project switching by unchecking `Preferences>Package Settings>CodeKit Commands>Enable Auto Switch CodeKit Project` and manually change the active project in CodeKit from Sublime via the Command Palette commands `CodeKit Select project` or `CodeKit Select framework`.

###Adding projects to CodeKit
If you're currently working on a project or framework that CodeKit doesn't know about, simply run the command `CodeKit Add project` or `CodeKit Add framework` from the Command Palette. From there you'll be presented with a list of folders specific to your current Sublime project to select from.

###Auto-pausing CodeKit
By default this plug-in will pause CodeKit when you're not focused on Sublime Text. This can be useful if you use the CLI or third-party tools to handle source control.

CodeKit states:
>Before you perform any action that will change large numbers of files at once (switching branches, rebasing, pull requests, etc.) you MUST tell CodeKit to ignore file changes.

If you'd rather handle toggling the paused state of CodeKit you can disable this feature by unchecking `Preferences>Package Settings>CodeKit Commands>Enable Auto Pausing` and run the `CodeKit pause` and `CodeKit unpause` commands from the Command Palette.

_Heads Up:_ These two commands are hidden from the Command Palette when auto-pausing is enabled since they're useless otherwise.

_Info:_ More details about why it's good practice to pause and other critical things to know about CodeKit can be found [here](http://incident57.com/codekit/help.html#critical-things).

###Launching and refreshing browsers
You have access to browser refreshing, style sheet reloading, browser specific previewing all from the Command Palette. Just type `CodeKit` in the Command Palette to see the full list.

_Info:_ Any new commands added will always be prefixed with `CodeKit` for easy viewing/access.