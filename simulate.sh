
#!/usr/bin/env bash
path="$1"
if [ -e "$path"/main.lua ]; then path=`dirname "$path"`; fi
token=`/bin/tar -cz --exclude .git -C "$path" .|ssh -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`
ssh summitdebug@lunaapp1.dev1.int.corvisacloud.com $token
echo
echo '------ COMPLETE ------'
read pause
