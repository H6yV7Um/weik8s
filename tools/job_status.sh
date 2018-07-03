#!bin/bash
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when "$0
	exit
fi
python -c "import sys,yarn_operation;print sys.argv;yarn_operation.yarn_kill(sys.argv[1])" $*
