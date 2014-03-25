
#!/bin/bash
# path="$1"
# if [ -e "$path"/main.lua ]; then path=`dirname "$path"`; fi

token=`/bin/tar -cz --exclude .git -C "/home/tkells/dev/summit_apps/tjtest/" .|ssh -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`

echo $token

/usr/bin/xterm -e /bin/bash -c "ssh -t summitdebug@lunaapp1.dev1.int.corvisacloud.com $token; echo; echo 'press any key to continue'; read -n 1" &

echo
echo '------ COMPLETE ------'
read pause
