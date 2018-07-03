# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/24. 

import sys,os
import json
import urllib2

from utils.logger import logger
from utils import weibox_macros 

file_name = __name__.upper()

from utils import weibox_macros
from utils import helpers
from read_yarn_app_id import read_yarn_app_id
import job_status_update

def yarn_log_app_id(_yarn_app_id = ""):
    if("NULL_YARN_APPLICATION_ID" == _yarn_app_id):
        return
    return yarn_run("yarn logs -applicationId %s" % _yarn_app_id)

def yarn_log(_job_key = ""):
    yarn_app_id = read_yarn_app_id(_job_key)
    return yarn_log_app_id(yarn_app_id)

def yarn_query_job_key(_job_key = ""):
    yarn_app_id = read_yarn_app_id(_job_key)
    state = yarn_job_status(yarn_app_id)
    trace_url = job_trace_url(yarn_app_id)
    return job_status_update.job_update(_job_key, state, trace_url, "")

def yarn_kill_app_id(_yarn_app_id = ""):
    if("NULL_YARN_APPLICATION_ID" == _yarn_app_id):
        return
    return yarn_run("yarn application -kill %s" % _yarn_app_id)

def yarn_kill(_job_key = ""):
    yarn_app_id = read_yarn_app_id(_job_key)
    return yarn_kill_app_id(yarn_app_id)

def yarn_run(_cmd = ""):
    cmd = weibox_macros.YARN_CONFIG + _cmd
    return helpers.sys_run(cmd)

def yarn_popen(_cmd = ""):
    cmd = weibox_macros.YARN_CONFIG + _cmd
    return helpers.sys_popen(cmd)

def yarn_job_query(_yarn_app_id = ""):
    if("NULL_YARN_APPLICATION_ID" == _yarn_app_id):
        return
    yarn_job_query_interface = yarn_master_detect() + weibox_macros.YARN_APP_WS_INTERFACE % _yarn_app_id
    return helpers.get(yarn_job_query_interface)

def yarn_job_status(_yarn_app_id = ""):
    if("NULL_YARN_APPLICATION_ID" == _yarn_app_id):
        return "WAITING"
    func_name = sys._getframe().f_code.co_name
    try:
        app_info = json.loads(yarn_job_query(_yarn_app_id))
    except Exception,e:
        print file_name,func_name,e.message
        return "LOST"
    job_state = helpers.get_value("app.state",app_info)
    if("" == job_state or None == job_state):
        return "LOST"
    else:
        return job_state

# disable the redirect url
class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response

# detect rm master real ip url
def yarn_master_detect():
    opener = urllib2.build_opener(NoRedirection)
    try:
        if(len(opener.open(weibox_macros.YARN_RM_MASTER_0).readlines()) == 0):
            rm_ip = weibox_macros.YARN_RM_MASTER_0
        else:
            rm_ip = weibox_macros.YARN_RM_MASTER_1
    except Exception,e:
        logger.error(e.message)
    return rm_ip

def job_trace_url(_yarn_app_id =""):
    if("NULL_YARN_APPLICATION_ID" == _yarn_app_id):
        return
    opener = urllib2.build_opener(NoRedirection)
    job_url = yarn_master_detect() + weibox_macros.YARN_APP_INTERFACE % _yarn_app_id
    return job_url