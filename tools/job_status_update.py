# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/23.
import sys,os
import json

import utils.weibox_macros
from utils.logger import logger
from utils import helpers


def job_update(_job_key = "", _status = "", _job_url = "", _log_url = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    job_status_interface = utils.weibox_macros.CC_JOB_UPDATE_INTERFACE
    job_update_url = job_status_interface + "&jobUrl=%s&logUrl=%s&jobStatus=%s" % (_job_url,_log_url,_status)
    job_update_url = job_status_interface
    param_update = {"jobKey" : _job_key, "jobUrl" : _job_url, "logUrl" : _log_url, "jobStatus" : _status}
    return helpers.post(job_update_url, param_update, "basic")

def job_query(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    try:
        response_info = helpers.get(utils.weibox_macros.CC_JOB_QUERY_INTERFACE % _job_key)
        response_obj = json.loads(response_info)
    except Exception,e:
        logger.error(e.message + "at %s." % file_name)
    return response_obj

def job_status_update(_job_key = "", _status = ""):
    response_obj = job_query(_job_key)
    job_url = helpers.get_value("result.jobUrl", response_obj)
    log_url = helpers.get_value("result.logUrl", response_obj)
    return job_update(_job_key=_job_key, _status= _status, _job_url=job_url, _log_url=log_url)

def job_job_url_update(_job_key = "", _job_url = ""):
    response_obj = job_query(_job_key)
    status = helpers.get_value("result.status", response_obj)
    log_url = helpers.get_value("result.logUrl", response_obj)
    return job_update(_job_key=_job_key, _job_url=_job_url, _status= status, _log_url=log_url)

def job_log_url_update(_job_key = "", _log_url = ""):
    response_obj = job_query(_job_key)
    job_url = helpers.get_value("result.jobUrl", response_obj)
    status = helpers.get_value("result.status", response_obj)
    return job_update(_job_key=_job_key, _log_url=_log_url, _status= status, _job_url=job_url)


if __name__ == '__main__':
    if(len(sys.argv) != 3):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    job_status = sys.argv[2]
    print job_status_update(job_key, job_status)
