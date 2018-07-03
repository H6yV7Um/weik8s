# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2017/12/12. 

import json,sys,os
import urllib,urllib2

# CC_HOST="http://10.77.29.69:8080"
CC_HOST="http://controlcenter.ds.sina.com.cn/"
CC_VERSION="/waic/weibox"
CC_INTERFACE="/job?jobKey=%s"
# HOST_NAME="http://10.77.29.69:8080/waic/weibox/job?jobKey=%s"
HOST_NAME="%s%s%s" % (CC_HOST, CC_VERSION, CC_INTERFACE)

class logger():
    @classmethod
    def debug(cls, msg = ""):
        # print "[DEBUG] : %s " % msg
        pass

    @classmethod
    def info(cls, msg = ""):
        print "[INFO] : %s " % msg

    @classmethod
    def warn(cls, msg = ""):
        print "[WARN] : %s " % msg

    @classmethod
    def error(cls, msg = ""):
        print "[ERROR] : %s " % msg
        exit(1)

def callback(_json_str = ""):
    return _json_str

def dict_format(_dict = {}):
    return json.dumps(_dict,sort_keys=True, indent=4, separators=(',',': '))

def json_format(_json_str = ""):
    return dict_format(json.loads(_json_str))

def get(_url):
    try:
        logger.debug("URL : " + _url)    #输出查看编码后的数据格式
        response = urllib2.urlopen(_url)
        req_info = response.read()
        logger.debug("%s" % req_info)
        return req_info
    except (urllib2.HTTPError, Exception),e:
        logger.error(e)
        exit(1)

def get_root_value(_key = "", _dict = {}):
    support_key = {"message":"", "result":"", "params":"", "code":""}
    rst = None
    if(support_key.has_key(_key)):
        if(_key == "result"):
            rst = _dict.get("result")[0]
        else:
            rst = _dict.get(_key)
    else:
        logger.error("found error key when parse job_json root value!!")
    return rst 

def get_value_naive(_key_path = "cluster.json.weibox_path", _dict = {}):
    tmp_obj = _dict
    path_tree = _key_path.strip().split(".")
    for key in path_tree:
        # tmp_obj = tmp_obj.get("key")
        tmp_obj = tmp_obj.get(key)
        if(tmp_obj == None):
            exit(1)
        if(isinstance(tmp_obj,list)):
            tmp_obj = tmp_obj[0]
    return tmp_obj

def get_value(_key_path = "cluster.json.weibox_path", _dict = {}):
    if(_dict == None):
        return ""
    tmp_obj = _dict.get(_key_path)
    if(tmp_obj == None):
        point_idx = _key_path.find(".")
        if(point_idx < 0):
            return ""
        tail_dict = _dict.get(_key_path[0:point_idx])
        if(isinstance(tail_dict,list)):
            tail_dict = tail_dict[0]
        tmp_obj = get_value(_key_path[point_idx+1:], tail_dict)
        # return tmp_obj if (not isinstance(tmp_obj, list)) else tmp_obj[0]
    # else:
    #     return tmp_obj
    return tmp_obj

def get_obj(_key_path = "result.cluster.json.weibox_path", _dict = {}):
    tmp_obj = _dict
    path_tree = _key_path.strip().split(".")
    for key in path_tree:
        # tmp_obj = tmp_obj.get("key")
        tmp_obj = tmp_obj.get(key)
        if(tmp_obj == None):
            exit(1)
    return tmp_obj


def get_args(_job_key = "", _key = ""):
    control_center_job_url = HOST_NAME % _job_key
    req_json = get(control_center_job_url)
    req_dict = json.loads(req_json) if (
        req_json.startswith("{") or
        req_json.startswith("[") ) else eval(req_json)
    return get_value(_key, req_dict)

def main(_args = []):
    if(len(_args) != 3):
        logger.error("parameter error in python! JOB_KEY,JSON_KEYS")

    _job_key = _args[1]
    _key = _args[2]
    print get_args(_job_key, _key)
    return 0

if __name__ == '__main__':
    main(sys.argv)
