#!/bin/bash
path="$1"
simulator_host="$2"
build_args=${*:3}

echo "Deploying project to test server..."
token=`tar -cz --exclude .git -C $path .|ssh -q debug@$simulator_host`

echo "Running simulator..."

osascript <<END
	tell application "Terminal"
	    tell window 1
	    	activate
	        set w to do script "clear; bash -c \"ssh -t summitdebug@$simulator_host '$token $build_args'; echo; echo Press any key to continue; read -n 1; exit\""
	    end tell
    end tell
END
