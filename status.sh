#!bin/bash
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when "$0
	exit
fi
#python -c "import sys,tools.yarn_operation;print sys.argv;tools.yarn_operation.yarn_query_job_key(sys.argv[1])" $*
python ${SELF_DIR}/tools/job_status.py ${JOB_KEY} >> weibox_status.log