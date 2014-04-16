#SummitEditor

SummitEditor is the official [http://www.sublimetext.com/3](Sublime Text 3) plugin for [http://corvisacloud.com]
(CorvisaCloud, LLC's) Summit platform. It provides you with useful snippets, syntax highlighting, and most importantly, access to the Summit Simulator.

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

Once the package has been installed there are a handful of configuration changes to be made in order to start simulating your code. All simulations require

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
