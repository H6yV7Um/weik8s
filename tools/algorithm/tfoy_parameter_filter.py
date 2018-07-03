# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/4/9.

import helpers
import get_args
import job_status_update

def gen_run_command(response_obj=''):
    return "export HADOOP_CONF_DIR=/etc/emr-gpu-yarn/hadoop-conf-2.7.2-1.2.99;\n" \
           "sh -x " + get_args.get_value("result.runCommand", response_obj)

def tfoy_json_convert_to_paramters(_json_obj = {}, _job_key=""):
    response_obj = job_status_update.job_query(_job_key)
    return gen_run_command(response_obj=response_obj)

