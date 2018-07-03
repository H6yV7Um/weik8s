# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/22. 

import sys,os
import re,json

from utils import weibox_macros
from utils.logger import logger
from utils import helpers
import job_status_update


def resolve_yarn_app_id(args = []):
    appIdLines = filter(lambda _key: (_key.find("application_") >= 0 ),args)
    if(len(appIdLines) > 0) :
        appIdLine = appIdLines[-1]
        YARN_REGEX_PATTERN="""(application_(\d+)_(\d+))"""
        re_search_rst = re.findall(YARN_REGEX_PATTERN, appIdLine)
        if(re_search_rst != None and len(re_search_rst) > 0):
            appId = re.compile(YARN_REGEX_PATTERN).findall(appIdLine)[-1][0]
            return appId
        else:
            return "NULL_YARN_APPLICATION_ID"
    else:
        return "NULL_YARN_APPLICATION_ID"

    # if __name__ == '__main__':
    # print __name__
    # print read_yarn_app_id(sys.argv)

def read_yarn_app_id(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    file_dir_name = os.path.dirname(os.path.abspath(__file__))
    job_status_interface = weibox_macros.CC_JOB_UPDATE_INTERFACE
    job_space = helpers.job_space(_job_key)
    job_trace_log_file = job_space + weibox_macros.WEIBOX_LOG
    logger.info("JOB_TRACE_LOG_FILE : %s." % job_trace_log_file)
    try:
        job_log_content = open(job_trace_log_file).read()
        yarn_app_id = resolve_yarn_app_id([job_log_content])
    except Exception,e:
        logger.error(func_name + " : " + e.message)
    return yarn_app_id

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print read_yarn_app_id(job_key)

