#SummitEditor

SummitEditor is the official [Sublime Text 3](http://www.sublimetext.com/3) plugin for [Corvisa LLC's]
(http://corvisa.com) Summit platform. It provides you with useful snippets, syntax highlighting, and most importantly, access to the Summit Simulator.

##Installation

###Requirements
All platforms require git, bash, and ssh to be installed and on the system path. There are additional requirements for windows and linux listed below.

*Windows*
* Git must be installed to the default location, this will be made more configurable in future updates.
* The git/bin directory must be on the system path.
* If not on the path already, git, bash, and ssh can be put on the path by selecting the "Use Git and optional Unix tools from the Windows Command Prompt" option on the "Adjusting your PATH environment" step of the git installer.

*Linux*
* Xterm must be installed and on the system path. This should be more flexible in future updates.

###Package installation
The recommended way to install SummitEditor is through Package Control. If you do not have Package Control installed, read the [installation instructions](https://sublime.wbond.net/installation). To install via Package Control:

1. Bring up the Command Palette (`ctrl+shift+p` or `cmd+shift+p` on Mac) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.
2. When the plugin list appears, type `SummitEditor`. Among the entries you should see `SummitEditor`. If that entry is not highlighted, use the keyboard or mouse to select it.

Optionally, you can use git to clone this repository into your Sublime Text `Packages` directory. You can confirm that installation has worked by opening the Command Palette and typing the word `summit`. You should see an available syntax option for `Lua (Summit)`.

###Optional Packages
SummitEditor also offers a [SummitLinter](https://github.com/corvisa/SummitLinter) plugin for [SublimeLinter 3](http://www.sublimelinter.com/en/latest/) allowing for automatic linting of your code. To install SummitLinter (as well as SublimeLinter if it is not already installed), first make sure you meet the [requirements](https://github.com/corvisa/SummitLinter#installation), then select `Tools > SummitEditor > Install SummitLinter Packages`. Note: using this option requires Package Control to be installed.

###Application Structure
When you clone your application, the application directory should be as follows:
```
<application>
├── assets/
├── spec/
├── src/
└── REPOCONF

```
The simulator will run the `main.lua` file inside the application's `src` directory.

##Running The Simulator

Once the package has been installed there are a handful of configuration changes to be made in order to start simulating your code. All simulations require that your code be in a SublimeText project. This can be done easily by cloning your code into a directory, then using `File -> Open Folder` to open the files. Once this has been done you can create a project from this open set of files by going to `Project -> Save Project As...`.

Now that you have a project created, we need to add some simulator settings to it. Simply go to `Project -> Edit Project` and add the following:

```json
"build_path": "/folder/that/contains/your/application/source"
```
build_path should point to the `src` directory's parent directory and *not* the `src` directory itself. There are also a few other optional parameters, which will allow you to connect to your live datastore from the simulator. You need to include all of the following:
```json
"application_id": "12345678-1234-5678-1234-567812345678",
"api_key": "bl53y1g3l5AS",
"api_secret": "bkas34n23=2",
"use_live_datastore": "true"
```
You can generate an API Key and Secret in your Summit Account under `Access -> API Keys`. Your Application ID is available in the Applications grid. Hover over a column header and click the arrow that appears. You will see a menu with additional columns, including "Application ID". Alternatively, your Application ID is available as the UUID at the end of your git remote.

Your final Project settings file should look something like this (if your app was in `/home/myuser/code/DemoApp/`:
```json
{
    "folders":
    [
        {
            "follow_symlinks": true,
            "path": "/home/myuser/code/DemoApp"
        }
    ],
    "build_path": "/home/myuser/code/DemoApp",
    "application_id": "12345678-1234-5678-1234-567812345678",
    "api_key": "bl53y1g3l5AS",
    "api_secret": "bkas34n23=2",
    "use_live_datastore": "true"
}
```

With these settings configured, you can start the simulation in one of two ways. First you must have the syntax settings of your file set to `Lua (Summit)` or you can manually select your build script from `Tools -> Build System`. If you need to do a simple simulation (one that does not require any special flags), you can now simply press `ctrl+b` on Windows or Linux machines and `cmd-b` on Mac computers. This should cause a terminal window to open on your screen allowing you to interact with your simulated application.

If your application requires additional flags to be set before being run you can start your build with `ctrl+shift+b` on Windows and Linux or `cmd+shift+b` on Mac computers. This will open an options panel on the bottom of the screen. This options panel accepts arguments prefixed with dashes and separated by spaces, ex - `--DNIS 5558675309 --ANI 5554441212`. A complete list of options is as follows:

| Option    | Detail            | Example                |
| ---------:| :---------------- | :--------------------- |
| DNIS      | Sets the DNIS or "number dialed", useful for testing number based routing. | `--DNIS 15558675309` | 
| ANI       | Sets the ANI or "number app called from", useful for doing things like looking up existing customers by phone number. | `--ANI 15551234567` | 
| test      | Runs your unit tests instead of opening the simulator. | `--test` | 
| verbose   | Should only be used in conjunction with `test`; This will output the full coverage report for your application (line by line), allowing you to see where you are missing test coverage. | `--test --verbose` | 

##License
The MIT License (MIT)

Copyright (c) 2014 Corvisa LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
