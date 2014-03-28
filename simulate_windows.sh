#!bash
project_path="$1"


export PATH=$PATH:"/c/Program Files (x86)/Git/bin":
echo "Compressing project..."
token=`tar -cz --exclude .git -C $project_path .|ssh -i /c/Users/tj.kells/.ssh/id_rsa -q summitdebug@lunaapp1.dev1.int.corvisacloud.com`
clear
echo "Deploying project to test server..."
echo "Running simulator..."

bash -c "ssh -i /c/Users/tj.kells/.ssh/id_rsa -t summitdebug@lunaapp1.dev1.int.corvisacloud.com "$token ${@:2}"; echo; echo 'Press any key to continue'; read -n 1" &

"C:\Program Files (x86)\Git\bin\sleep" 20