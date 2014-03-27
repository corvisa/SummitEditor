#!/bin/bash
path="$1"

echo "Deploying project to test server..."
token=`tar -cz --exclude .git -C $path .|ssh -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`

echo "Running simulator..."

osascript <<END
	tell application "Terminal"
	    tell window 1
	    	activate
	        set w to do script "clear; bash -c \"ssh -t summitdebug@lunaapp1.dev1.int.corvisacloud.com '$token ${@:2}'; echo; echo Press any key to continue; read -n 1; exit\""
	    end tell
    end tell
END
