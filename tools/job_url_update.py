# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/23.
import sys,os
import json

from utils import weibox_macros
from utils.logger import logger
from utils import helpers
import job_status_update
import yarn_operation
from read_yarn_app_id import read_yarn_app_id

def job_url_update(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    file_dir_name = os.path.dirname(os.path.abspath(__file__))
    job_status_interface = weibox_macros.CC_JOB_UPDATE_INTERFACE
    job_space = helpers.job_space(_job_key)
    job_trace_log_file = job_space + "/weiflow-from-weiclient.log"
    job_status = ""
    try:
        # job submit failed
        if(not os.path.isdir(job_space)):
            job_status_update.job_status_update(_job_key, "FAILED")
        # job run failed
        elif(not os.path.isfile(job_trace_log_file)):
            job_status_update.job_status_update(_job_key, "LOST")
        # job run successed.
        else:
            yarn_app_id = read_yarn_app_id(_job_key)
            # job not fount applicationId : submitted just now or has no applicationId
            if("NULL_YARN_APPLICATION_ID" == yarn_app_id):
                job_status_update.job_status_update(_job_key, "WAITING")
            else:
                log_url = weibox_macros.CC_JOB_LOG_URL_INTERFACE % _job_key
                job_url = yarn_operation.job_trace_url(yarn_app_id)
                # job_status = json.loads(com.weibo.weibox.yarn.tools.yarn_operation.yarn_job_query(yarn_app_id)).get("app").get("state")
                job_status = yarn_operation.yarn_job_status(yarn_app_id)
                job_status_update.job_update(_job_key=_job_key, _status=job_status, _job_url= job_url, _log_url= log_url)
    except Exception,e:
        logger.error(func_name + " : " + e.message)
    return job_status

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print job_url_update(job_key)
