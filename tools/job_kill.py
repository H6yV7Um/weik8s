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
import commands 

Known_submit_type = ['dataflow', 'lda', 'lr', "tfoy"]

def job_prepare(_job_key = ""):
    # checke the job_key
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    _key = "result.json"
    rst_json = get_args.get_args(_job_key, _key)
    specified_submit_type = rst_json.get("job_common_submit_type")
    
    return rst_json

def assembleCmd(_job_key = ""):
    submit_cmd = "arena delete "
    rst_json = job_prepare(_job_key)
    submit_cmd += rst_json.get("job_name")
    return submit_cmd

def job_kill(_job_key = ""):
    # checke the job_key
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    kill_cmd = assembleCmd(_job_key)
    print("arena delete cmd: %s " % kill_cmd)
    
    try:
        #sys_run_code = helpers.sys_run(kill_cmd)
        status, output = commands.getstatusoutput(kill_cmd)
        print("status code :%s" % status)
        #print("sys run code :%s" % sys_run_code)
        #if(0 == status):
            #job_url_update.job_url_update(_job_key)
            #job_space = helpers.job_space(_job_key)
            #if(os.path.isdir(job_space)):
                #import shutil
                #shutil.rmtree(job_space)
    except Exception,e:
        logger.warn(e)
    
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print job_kill(job_key)
