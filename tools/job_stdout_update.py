# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/23.
import sys,os
import json

import utils.weibox_macros
from utils.logger import logger
from utils import helpers
import job_status_update

def job_stdout_update(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    file_dir_name = os.path.dirname(os.path.abspath(__file__))
    job_stdout_interface = utils.weibox_macros.CC_JOB_STDOUT_INTERFACE
    job_space = helpers.job_space(_job_key)
    job_log_file = job_space + "/weiflow-from-weiclient.log"
    param_value = {"jobKey" : _job_key, "file" : job_log_file}
    return helpers.post(job_stdout_interface,param_value,"stdout")


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print job_stdout_update(job_key)
