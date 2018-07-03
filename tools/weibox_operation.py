# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/24. 
import json,sys,os
import urllib,urllib2
from utils.logger import logger
from utils import helpers
import job_status_update

def job_seperate(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key, func_name, file_name)
    #response_obj = job_status_update.job_query(_job_key)
    #code_path = helpers.get_value("result.codePath", response_obj)
    job_space = helpers.job_space(_job_key)
    if(os.path.isdir(job_space)):
        import shutil
        shutil.rmtree(job_space)
    mkdir_response_code = os.makedirs(job_space)
    print("mkdir code:%s" % mkdir_response_code)
    #rsync_response_code = 0
    #if("null" != code_path):
        #rsync_response_code = helpers.sys_run("rsync -zr --progress 10.77.29.68::backup/weiflow/%s/* %s/" % (code_path,job_space))
    return mkdir_response_code# or rsync_response_code


def ref_load(_job_common_submit_type = "lda"):
    _module_name = "algorithm.{submit_type}_parameter_filter".format(submit_type = _job_common_submit_type)
    _func_name = "{submit_type}_json_convert_to_paramters".format(submit_type = _job_common_submit_type)
    if(sys.modules.has_key(_module_name)):
        del sys.modules[_module_name]
    try:
        modules_client = __import__(_module_name, fromlist = True)
    except ImportError:
        print "ImportError: No module named %s" % _module_name
        print "please check you command usage."
        exit(1)
    assert hasattr(modules_client,_func_name),  "could not find function for {func_name},".format(func_name = _func_name) + \
                                           " please check parameters from weiclient."
    obj_func = getattr(modules_client,_func_name,None)
    return obj_func


