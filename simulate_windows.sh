export PATH=$PATH:"/c/Program Files (x86)/Git/bin":

keyfile="$HOMEDRIVE$HOMEPATH\\.ssh\\id_rsa"
project_path="$1"

echo "Compressing project..."
token=`tar -cz --exclude .git -C $project_path .|ssh -i "$keyfile" -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`
echo "Deploying project to test server..."

clear

echo "Running simulator..."

ssh -t -t -i "$keyfile" summitdebug@lunaapp1.dev1.int.corvisacloud.com $token ${@:2}
echo 'Press any key to continue'
read -n 1