#SummitEditor

<<<<<<< HEAD
SummitEditor is the official [http://www.sublimetext.com/3](Sublime Text 3) plugin for [http://corvisacloud.com]
(CorvisaCloud, LLC's) Summit platform. It provides you with useful snippets, syntax highlighting, and most importantly, access to the Summit Simulator.
=======
SummitEditor is the official [Sublime Text 3](http://www.sublimetext.com/3) plugin for [CorvisaCloud, LLC's]
(http://corvisacloud.com) Summit platform. It provides you with useful snippets, syntax highlighting, and most importantly, access to the Summit Simulator.
>>>>>>> 417a703f6c8e98cad45d710eed29e4192b7e5864

##Installation

###Requirements
All platforms require git, bash, and ssh to be installed and on the system path. There are additional requirements for windows and linux listed below.

*Windows*
* Git must be installed to the default location, this will be made more configurable in future updates.
* The git/bin directory must be on the system path.

*Linux*
* Xterm must be installed and on the system path. This should be more flexible in future updates.

To install the plugin, simply use git to clone this repository into your sublime text packages directory. You can confirm that this has worked by opening the command palette `ctrl+shift+p` and typing the word 'summit'. You should see an available syntax option for `Lua (Summit)`.


##Running The Simulator

<<<<<<< HEAD
Once the package has been installed there are a handful of configuration changes to be made in order to start simulating your code. All simulations require
=======
Once the package has been installed there are a handful of configuration changes to be made in order to start simulating your code. All simulations require that your code be in a SublimeText project. This can be done easily by cloning your code into a directory, then using `File -> Open Folder` to open the files. Once this has been done you can create a project from this open set of files by going to `Project -> Save Project As...`.

Now that you have a project created, we need to add some simulator settings to it. Simply go to `Project -> Edit Project` and add the following:

```json
"build_path": "/folder/that/contains/your/application/source"
```
You can also optionally add the application id, which can be useful for simulation involving data in datastores:
```json
"application_id": "12345678-1234-5678-1234-567812345678"
```
With these settings configured, you can start the simulation in one of two ways. First you must have the syntax settings of your file set to `Lua (Summit)` or you can manually select your build script from `Tools -> Build System`. If you need to do a simple simulation (one that does not require any special flags), you can now simply press `ctrl+b` on Windows or Linux machines and `cmd-b` on Mac computers. This should cause a terminal window to open on your screen allowing you to interact with your simulated application.

If your application requires additional flags to be set before being run you can start your build with `ctrl+shift+b` on Windows and Linux or `cmd+shift+b` on Mac computers. This will open an options panel on the bottom of the screen. This options panel accepts arguments prefixed with dashes and separated by spaces, ex - `--DNIS 5558675309 --ANI 5554441212`. A complete list of options is as follows:

| Option    | Detail            |
| ---------:| ----------------- |
| DNIS      | Sets the DNIS or "number dialed", useful for testing number based routing. |
| ANI       | Sets the ANI or "number app called from", useful for doing things like looking up existing customers by phone number |
| appid     | Attempt to set the running application's ID. This will give your datastores the proper context but all requests to this flag hit SSH key authentication. If an invalid appid is specified, the simulator will raise an error. This flag is passed automatically via project setting `application_id` |
| debug     | In the case of an error being raised inside of your application, drop into an interactive shell for further debugging. |

>>>>>>> 417a703f6c8e98cad45d710eed29e4192b7e5864

##License
The MIT License (MIT)

Copyright (c) 2014 CorvisaCloud, LLC

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
