#!/bin/bash
path="$1"
simulator_host="$2"
build_args=${*:3}

token=`/bin/tar -cz --exclude .git -C $path .|ssh -q summitdebug@$simulator_host`
/usr/bin/xterm -geometry 120x50 -e /bin/bash -c "echo 'Running simulator...'; ssh -t summitdebug@$simulator_host '$token $build_args'; echo; echo 'Press any key to continue'; read -n 1" &
