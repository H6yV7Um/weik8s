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
import commands
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
    weibox_operation.job_seperate(_job_key)
    _key = "result.json"
    rst_json = get_args.get_args(_job_key, _key)
    
    # job prepared. ready
    job_status_update.job_status_update(_job_key = _job_key, _status = "ready")
    return rst_json

def get_envs(rst_json):
    result = {}
    envs = []
    job_envs = rst_json.get("job_docker_envs")
    print(job_envs)
    #if not job_envs is None and len(str(job_envs)) > 0:
    if job_envs is not None:
        envs = job_envs.split(",")
        for i in range(len(envs)):
            item = envs[i].split("=")
            result[item[0]]=item[1]
    return result

def assemble_cmd(rst_json, _job_key):
    submit_cmd = "arena submit"
    #rst_json = job_prepare(_job_key)
    envs = get_envs(rst_json)
    print("envs : %s" % envs)
    code_path = get_args.get_args(_job_key, "result.codePath") 
    sync_source = "10.77.29.68::backup/weiflow/" + code_path
    work_path = "/root/" + code_path
    print("syncSource: %s" % sync_source)
    submit_cmd += " --name=" + rst_json.get("job_name")
    gpus = rst_json.get("job_gpu_num_per_node")
    if gpus is not None and len(str(gpus)) >0:
        submit_cmd += " --gpus=" + rst_json.get("job_gpu_num_per_node") 
    cpu = rst_json.get("job_cpu_num_per_node")
    if cpu is not None and len(str(cpu)) >0:
        submit_cmd += " --cpu=" + rst_json.get("job_cpu_num_per_node") 
    memory = rst_json.get("job_memory_allocated")
    if memory is not None and len(str(memory)) >0:
        submit_cmd += " --memory=" + rst_json.get("job_memory_allocated") 
    mode = rst_json.get("job_running_mode")
    if mode is not None and len(str(mode)) > 0:
        submit_cmd += " --mode=" + rst_json.get("job_running_mode")
    works = rst_json.get("job_worker_num")
    if works is not None and len(str(works)) >0:
        submit_cmd += " --workers=" + rst_json.get("job_worker_num")
    for key in envs:
        submit_cmd += " --env="+key+"="+envs[key]
    submit_cmd += " --image=" + rst_json.get("job_docker_image")
    if str(rst_json.get("job_running_mode")) == "horovod":
        submit_cmd += " --sshPort=33"
    submit_cmd += " --syncMode=rsync"
    submit_cmd += " --syncSource=" + sync_source
    submit_cmd += " --workingDir=/root"
    if len(str(rst_json.get("job_start_docker_command"))) >0:
        submit_cmd += ' "' + 'cd ' + work_path + ";" + rst_json.get("job_start_docker_command") + '"'
        #submit_cmd += ' "' + rst_json.get("job_start_docker_command") + '"'
    return submit_cmd

def get_log_url(rst_json):
    log_cmd = "arena logviewer " + rst_json.get("job_name") 
    r = os.popen(log_cmd)
    info = r.readlines()
    url = info[1].replace("\r","")
    url = url.replace("\n","")
    return url

def get_job_url(log_url):
    prefix = "10.87.217.210:9090/#!/job/default/"
    sufix = "?namespace=default"
    url_array = log_url.split("/")
    pod_name = url_array[4]
    job_name = pod_name[:-6] 
    return prefix + job_name + sufix
    
def job_submit(_job_key = ""):
    # checke the job_key
    func_name = sys._getframe().f_code.co_name
    file_name = __name__.upper()
    helpers.job_key_check(_job_key,func_name,file_name)
    rst_json = job_prepare(_job_key)
    job_status_update.job_status_update(_job_key = _job_key, _status = "acceptted")
    submit_cmd = assemble_cmd(rst_json, _job_key)
    print("arena submit cmd: %s " % submit_cmd)
    
    try:
        #sys_run_code = helpers.sys_run(submit_cmd)
        status, output = commands.getstatusoutput(submit_cmd)
        print("status code :%s" % status)
        print("output :%s" % output)
        if(0 == status):
            log_url = get_log_url(rst_json)
            print("log url:%s" % log_url)
            job_url = get_job_url(log_url)
            print("job url:%s" % job_url)
            job_log_url = job_url + "\n" + log_url
            #job_status_update.job_update(_job_key, "acceptted", log_url, "")
            job_status_update.job_update(_job_key, "acceptted", job_log_url, "")
            #job_space = helpers.job_space(_job_key)
            #log_cmd = "arena logs -f " + rst_json.get("job_name") + " >> " + job_space + "/weiflow-from-weiclient.log"
            #print("logs cmd:%s" % log_cmd)
            #status, output = commands.getstatusoutput(log_cmd)
            #job_url_update.job_url_update(_job_key)
            #job_status_update.job_status_update(_job_key = _job_key, _status = "finished")
        else:
            job_status_update.job_status_update(_job_key = _job_key, _status = "failed")
            print(output)
    except Exception,e:
        logger.warn(e)
        job_status_update.job_status_update(_job_key = _job_key, _status = "failed")
    
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logger.error("parameters error found when %s. " % __file__)
    job_key = sys.argv[1]
    print job_submit(job_key)
