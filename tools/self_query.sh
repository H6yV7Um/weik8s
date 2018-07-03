#!/usr/bin/env bash
JOB_KEY=$1
if [ "" = "${JOB_KEY}" ];then
    echo "parameters error when self_query."
	exit
fi
SELF_DIR="$( cd "$( dirname "$0" )" && pwd )"
sleep 55
sh ${SELF_DIR}/../log.sh ${JOB_KEY}
