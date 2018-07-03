#!/bin/bash
source /etc/profile
export KUBECONFIG=/root/.kube/config
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when "$0
	exit
fi
#python -c "import sys;from tools import yarn_operation;print sys.argv;yarn_operation.yarn_kill(sys.argv[1])" $*
python ${SELF_DIR}/tools/job_kill.py ${JOB_KEY} >> weibox_kill.log
