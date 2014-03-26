#!/bin/bash
path="$1"

echo "Deploying project to test server..."
token=`/bin/tar -cz --exclude .git -C $path .|ssh -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`

echo "Running simulator..."
/usr/bin/xterm -e /bin/bash -c "ssh -t summitdebug@lunaapp1.dev1.int.corvisacloud.com $token ${*:2}; echo; echo 'Press any key to continue'; read -n 1" &
