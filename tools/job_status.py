# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/23.
import sys,os
from utils.logger import logger
from utils import helpers
import job_status_update
import job_url_update
import weibox_operation
import yarn_operation
from utils import weibox_macros
from algorithm import get_args
import json

Known_submit_type = ['dataflow', 'lda', 'lr', "tfoy"]

def job_prepare(_job_key = ""):
    # checke the job_key
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    # update the status to cc show weibox received the job.
    job_status_update.job_status_update(_job_key = _job_key, _status = "submitting")
    
    response_obj = job_status_update.job_query(_job_key)
    target_user_cc = weibox_macros.submit_account(helpers.get_value("result.submitAccount", response_obj))


    # run_command = helpers.get_value("result.runCommand", response_obj)
    _key = "result.json"
    rst_json = get_args.get_args(_job_key, _key)
    specified_submit_type = rst_json.get("job_common_submit_type")
    
    # job prepared. ready
    job_status_update.job_status_update(_job_key = _job_key, _status = "ready")
    return rst_json


def assembleCmd(_job_key = ""):
    submit_cmd = "arena get"
    rst_json = job_prepare(_job_key)
    submit_cmd += " --name=" + rst_json.get("job_name")
    return submit_cmd

def job_status(_job_key = ""):
    # checke the job_key
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    job_status_update.job_status_update(_job_key = _job_key, _status = "acceptted")
    status_cmd = assembleCmd(_job_key)
    print("arena status cmd: %s " % status_cmd)
    '''
    try:
        sys_run_code = helpers.sys_run(submit_cmd)
        if(0 == sys_run_code):
            #job_url_update.job_url_update(_job_key)
            job_status_update.job_status_update(_job_key = _job_key, _status = "finished")
    except Exception,e:
        logger.warn(e)
        job_status_update.job_status_update(_job_key = _job_key, _status = "failed")
    '''
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print job_status(job_key)


