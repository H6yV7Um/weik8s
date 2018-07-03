# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/29. 
# CC_HOST="http://10.77.29.69:8080"
import os

WEIBOX_SUBMIT = "/weibox_submit.sh"
WEIBOX_LOG = "/weiflow-from-weiclient.log"

CC_HOST="http://controlcenter.ds.sina.com.cn"
CC_WEIBOX_VERSION="/waic/weibox"
HOST_NAME = CC_HOST + CC_WEIBOX_VERSION
# job query intercace
CC_JOB_QUERY_INTERFACE = HOST_NAME + "/job?jobKey=%s"
# job update intercace
CC_JOB_UPDATE_INTERFACE = HOST_NAME + "/job/update"
# job stdout update interface
CC_JOB_STDOUT_INTERFACE = HOST_NAME + "/job/stdout/update"
# job log url interface
CC_JOB_LOG_URL_INTERFACE = HOST_NAME.split("/weibox")[0] + "/job/stdout?jobKey=%s"


weibox_submit_script = """
CUR_DIR="$( cd "$( dirname "$0" )" && pwd )" 
chown -R ${TARGET_USER} ${CUR_DIR}
su - ${TARGET_USER} -s /bin/bash <<EOF
cd $CUR_DIR;
source ~/.bashrc
python ${CUR_DIR}/../../tools/job_status_update.py ${JOB_KEY} 'running'
${RUN_COMMAND} > "${CUR_DIR}"/weiflow-from-weiclient.log 2>&1 
echo "hello world."
exit; 
EOF
"""

def job_util_path():
    # return os.path.abspath(os.path.dirname(__file__))
    # return os.path.abspath(os.path.dirname(__file__))
    # return /data0/control_center/weibox/algorithm-weibox-v0.0.1/tools/utils
    # /data0/control_center/weibox/yarn-weibox/ksp weibox/ksp/${JOB_KEY}/
    # return os.path.abspath(weibox_macros.job_util_path() + "/../../ksp/%s" % _job_key)
    # Specify 10.77.29.69 abspath
    return os.path.abspath("/data0/control_center/weibox/k8s-weibox" + "/tools/utils")

# yarn config source command
YARN_CONFIG = "source %s/yarn-config;" % job_util_path()
# yarn Resource Manager
YARN_RM_MASTER_0 = "http://10.87.49.220:8088"
YARN_RM_MASTER_1 = "http://10.87.49.221:8088"
YARN_RM_MASTER_0 = "http://10.87.218.178:8088"
YARN_RM_MASTER_1 = "http://10.87.218.179:8088"
# yarn application interface
YARN_APP_INTERFACE = "/cluster/app/%s"
# yarn application restful interface
YARN_APP_WS_INTERFACE = "/ws/v1/cluster/apps/%s"


submit_account_mapping = {
    "weibo_bigdata_ba":"d1_weibo_bigdata_ba",
    "weibo_bigdata_hotmblog":"d1_weibo_bigdata_hotmblog",
    "weibo_bigdata_pa":"d1_weibo_bigdata_pa",
    "weibo_bigdata_push":"d1_weibo_bigdata_push",
    "weibo_bigdata_spam":"d1_weibo_bigdata_spam",
    "weibo_bigdata_sys":"d1_weibo_bigdata_sys",
    "weibo_bigdata_vf":"d1_weibo_bigdata_vf"
}

def submit_account(_target_submit_account = ""):
    return submit_account_mapping.get(_target_submit_account)

def submit_script_generator(_job_key = "",
                            _target_user = "d1_weibo_bigdata_pa",
                            _run_command = "scripts.sh"):
    script_cmd = "#!/usr/bin/env bash" + "\n"
    script_cmd += "TARGET_USER=%s" % _target_user + "\n"
    script_cmd += "RUN_COMMAND=%s" % _run_command + "\n"
    script_cmd += "JOB_KEY=%s" % _job_key + "\n"
    script_cmd += weibox_submit_script

    # script_cmd = "#!/usr/bin/env bash" + "\n"
    # script_cmd += "TARGET_USER=%s" % _target_user + "\n"
    # script_cmd += "RUN_COMMAND=%s" % _run_command + "\n"
    # script_cmd += "JOB_KEY=%s" % _job_key + "\n"
    # script_cmd += """
    #     CUR_DIR="$( cd "$( dirname "$0" )" && pwd )"
    #     cd $CUR_DIR;
    #     python ${CUR_DIR}/../../tools/job_status_update.py ${JOB_KEY} 'running'
    #     sh -x ${RUN_COMMAND} > "${CUR_DIR}"/weiflow-from-weiclient.log 2>&1 &
    #     echo "hello world."
    # """
    return script_cmd

