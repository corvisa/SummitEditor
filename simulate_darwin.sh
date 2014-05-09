#!/bin/bash
# The MIT License (MIT)

# Copyright (c) 2014 CorvisaCloud, LLC

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

path="$1"
simulator_host="$2"
simulator_user="$3"
build_args=${*:4}

echo "Deploying project to test server..."
token=`tar -cz --exclude .git -C $path .|ssh -q $simulator_user@$simulator_host`

echo "Running simulator..."

osascript <<END
	tell application "Terminal"
	    tell window 1
	    	activate
	        set w to do script "clear; bash -c \"ssh -t $simulator_user@$simulator_host '$token $build_args'; echo; echo Press any key to continue; read -n 1; exit\""
	    end tell
    end tell
END
