#!/bin/bash
source /etc/profile
export KUBECONFIG=/root/.kube/config
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when "$0
	exit
fi
python ${SELF_DIR}/tools/job_submit.py $* >> weibox_submit.log
