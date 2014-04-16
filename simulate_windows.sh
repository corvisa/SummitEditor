export PATH=$PATH:"/c/Program Files (x86)/Git/bin":

keyfile="$HOMEDRIVE$HOMEPATH\\.ssh\\id_rsa"
project_path="$1"
simulator_host="$2"
build_args=${*:3}

echo "Compressing project..."
token=`tar -cz --exclude .git -C $project_path .|ssh -i "$keyfile" -q debug@$simulator_host`
echo "Deploying project to test server..."

clear

echo "Running simulator..."

ssh -t -t -i "$keyfile" debug@$simulator_host $token $build_args
echo 'Press any key to continue'
read -n 1
