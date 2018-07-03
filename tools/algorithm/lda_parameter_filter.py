# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2017/12/19.

import json
import sys

import get_args
import logger
import get_sample_path

public_base_path = "hdfs://emr-cluster/user/feed_weibo/algorithm_platform"
public_log_path = public_base_path + "/log/{job_key}"
public_sample_path = public_base_path + "/sample/{job_key}"
public_model_path = public_base_path + "/model/{job_key}"

def gen_public_path_by_job_key(_job_key = ""):
    public_log_path_with_key = public_log_path.format(job_key=_job_key)
    public_sample_path_with_key  = public_sample_path.format(job_key=_job_key)
    public_model_path_with_key  = public_model_path.format(job_key=_job_key)

def sample_id_to_sample_path(_sample_id = "", _account = ""):
    _key = "result.locations"
    return get_sample_path.get_args(_sample_id, _key, _account = _account)

# "client_center_host_name": "http://10.77.29.69:8080",
str_args = u"""{"action.type": "train",
            "angel.am.log.level": "DEBUG",
            "angel.app.submit.class": "waic.ml.lda.LDARunner",
            "angel.job.name": "LDA",
            "angel.log.path": "hdfs://emr-cluster/user/feed_weibo/algorithm_platform/log/{job_key}" ,
            "angel.ps.log.level": "DEBUG",
            "angel.ps.memory.mb": "5000",
            "angel.ps.number": "3",
            "angel.save.model.path": "hdfs://emr-cluster/user/feed_weibo/algorithm_platform/model/{job_key}" ,
            "angel.worker.log.level": "DEBUG",
            "angel.worker.memory.mb": "8000",
            "angel.worker.task.number": "3",
            "angel.workergroup.number": "3",
            "center_user_name": "enzhao",
            "center_user_password": "sha1-password",
            "client_center_host_name": "http://controlcenter.ds.sina.com.cn/",
            "client_change_host": "true",
            "client_control_center_version": "waic",
            "client_job_path": "core-path",
            "cluster_dispatch_type": "yarn",
            "cluster_name": "rtCluster",
            "f": "./conf/weiclient.conf.angel.lda.simple.template",
            "file_name": "suanec-spark-yarn-angel-LDA-1512384802213843",
            "job_command": "job_submit.sh",
            "job_common_ip_preference": "10.77.26.68",
            "job_common_is_distributed": "1",
            "job_common_is_docker": "0",
            "job_common_is_gpu": "1",
            "job_common_resource": "0",
            "job_common_submit_jar": "_jar_path",
            "job_common_submit_node_id": "1",
            "job_common_submit_type": "spark",
            "job_common_submit_xml": "dataflow-pipeline.xml",
            "job_common_user_name_preference": "feed_ml",
            "job_docker_image": "core-image",
            "job_docker_tag": "core-tag",
            "job_is_tools_valid": "1",
            "job_log_command": "job_logs.sh",
            "job_name": "lda-00",
            "job_query_command": "job_status.sh",
            "job_stop_command": "job_delete.sh",
            "job_submit_command": "job_submit.sh",
            "job_tensorflow_gpu_num_pernode": "",
            "job_tensorflow_gpu_num_pertask": "1",
            "job_tensorflow_ps_number": "1",
            "job_tensorflow_ps_port": "2222",
            "job_tensorflow_worker_number": "2",
            "job_tensorflow_worker_port": "2223",
            "job_user_conf_path": "usr/usr.cmd",
            "job_user_log_path": "/work_dir/git_repo/train.log",
            "job_user_sample_path": "hdfs://10.87.49.220:8020/",
            "job_user_sample_type": "hdfs",
            "job_user_source_path": "ssh://git@10.13.1.213:2222/algorithm/ctr.git sb",
            "job_user_source_type": "git",
            "ml.epoch.num": "10",
            "ml.lda.alpha": "0.1",
            "ml.lda.beta": "0.2",
            "ml.lda.topic.num": "1000",
            "ml.lda.word.num": "100010",
            "ml.worker.thread.num": "4",
            "queue": "feed_weibo",
            "sample.id": "lda-test-sample",
            "save.doc.topic": "true",
            "model.id": "{job_key}",
            "model.owner": "gaolin3",
            "queue": "feed_weibo",
            "save.word.topic": "true"}"""

# "angel.train.data.path": "hdfs://emr-cluster/user/feed_weibo/algorithm_platform/sample/{job_key}" ,
# "model.url": "http://10.77.29.69:8080/waic/models/register?algorithm=LR&business=waic",
# "sample.id": "lda_test_1",
weiclient_args = str_args.replace("angel.","waic.")

known_parameters = [
    "action.type",
    "angel.am.log.level",
    "angel.app.submit.class",
    "angel.job.name",
    "angel.log.path",
    "angel.ps.log.level",
    "angel.ps.memory.mb",
    "angel.ps.number",
    "angel.train.data.path",
    "angel.save.model.path",
    "angel.worker.log.level",
    "angel.worker.memory.mb",
    "angel.worker.task.number",
    "angel.workergroup.number",
    "ml.epoch.num",
    "ml.lda.alpha",
    "ml.lda.beta",
    "ml.lda.topic.num",
    "ml.lda.word.num",
    "ml.worker.thread.num",
    "queue",
    "save.doc.topic",
    "save.word.topic"
]
known_parameters += ["model.url", "model.id", "model.owner", "sample.id"]

def init_default_known_parame():
    angel_json_dict = json.loads(str_args)
    return map(lambda x : (x,angel_json_dict.get(x)), known_parameters)

known_parameters_defaults = dict(init_default_known_parame())
need_default_key = {
    "angel.log.path" : public_log_path,
    "angel.train.data.path" : public_sample_path,
    "angel.save.model.path" : public_model_path,
    "model.id" : "{job_key}",
    "model.url": "http://controlcenter.ds.sina.com.cn/waic/models/register?algorithm=LDA&business=waic",
    "angel.ps.log.level" : "DEBUG",
    "angel.worker.log.level" : "DEBUG",
    "angel.am.log.level" : "DEBUG"
}

# waic parameter to angel parameter
dict_parameters = dict(map(lambda x : (x.replace("angel.", "waic."),x), known_parameters))

def lda_json_to_dict(_json_str = ""):
    json_dict_obj = json.loads(_json_str)
    json_parameters_value = map(
        lambda x :
        (dict_parameters.get(x), get_args.get_value(x, json_dict_obj)),
        dict_parameters.keys()
    )
    parameter_dict = known_parameters_defaults
    parameter_dict.update(dict(json_parameters_value))
    parameter_dict.update({"angel.job.name" : json_dict_obj.get("job_name")})
    parameter_dict["center_user_name"] = get_args.get_value("center_user_name", json_dict_obj)
    return parameter_dict

def lda_gen_submit_command_by_dict(_parameter_dict = {}, _job_key = ""):
    _parameter_dict["angel.app.submit.class"] = "com.tencent.angel.ml.lda.LDARunner"
    if(_parameter_dict.has_key("queue")):
        _parameter_dict.pop("queue")
    for key in need_default_key.keys():
        if((not _parameter_dict.has_key(key)) or _parameter_dict.get(key) == "" or _parameter_dict.get(key) == None):
            _parameter_dict[key] = need_default_key.get(key).format(job_key=_job_key)
    if(_parameter_dict.has_key("model.url")):
        seperated_url = _parameter_dict.get("model.url").replace("&","\&")
        _parameter_dict["model.url"] = seperated_url
    if(not _parameter_dict.has_key("sample.id")):
        logger.logger.error("lda training need sample id to find sample info.")
    else:
        center_user_name = _parameter_dict["center_user_name"]
        _parameter_dict["angel.train.data.path"] = \
            sample_id_to_sample_path(_parameter_dict["sample.id"], center_user_name)
        _parameter_dict.pop("center_user_name")
    str_for_angel = "angel-submit"
    for key in sorted(_parameter_dict.keys()):
        str_for_angel += " --%s %s" % (key, _parameter_dict.get(key))
    return str_for_angel

def lda_json_convert_to_paramters(_json_str = weiclient_args, _job_key = "" ):
    return lda_gen_submit_command_by_dict(lda_json_to_dict(_json_str), _job_key)

def lda_json_convert_to_paramters_in_one(_json_str = weiclient_args):
    json_dict_obj = json.loads(_json_str)
    json_parameters_value = map(
        lambda x :
        (dict_parameters.get(x), get_args.get_value(x, json_dict_obj)),
        dict_parameters.keys()
    )
    parameter_dict = dict(json_parameters_value)
    parameter_dict["angel.app.submit.class"] = "com.tencent.angel.ml.lda.LDARunner"
    if(parameter_dict.has_key("queue")):
        parameter_dict.pop("queue")
    str_for_angel = "angel-submit"
    for key in sorted(parameter_dict.keys()):
        str_for_angel += " --%s %s" % (key,parameter_dict.get(key))
    return str_for_angel


def main(_args = []):
    if(len(_args) != 2):
        print "[= %s =] passed for test in [@ %s @] " % (sys._getframe().f_code.co_name,  __name__.upper())
        logger.error("parameter error in python! JOB_KEY.")
        return 1
    _job_key = _args[1]
    _key = "result.json"
    rst_json = get_args.get_args(_job_key, _key)
    submit_command = lda_json_convert_to_paramters(json.dumps(rst_json), _job_key=_job_key)
    print submit_command
    return 0

if __name__ == '__main__':
    main(sys.argv)

