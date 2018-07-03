# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/23.
import sys,os
from utils.logger import logger
from utils import helpers
import job_url_update
import job_stdout_update

def job_log_and_update(_job_key = ""):
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    job_url_update(_job_key)
    job_stdout_update(_job_key)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    job_log_and_update(job_key)
