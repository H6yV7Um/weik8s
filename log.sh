#!bin/bash
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when "$0
	exit
fi
# python -c "import sys,tools.job_submit;print sys.argv;tools.job_submit.job_submit(sys.argv[1])" $*
# python ${SELF_DIR}/tools/job_stdout_update.py $*
python ${SELF_DIR}/tools/job_url_update.py ${JOB_KEY}
