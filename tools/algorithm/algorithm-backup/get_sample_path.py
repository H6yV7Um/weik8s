# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2017/12/26. 

import json,sys,urllib,urllib2
from logger import logger

CC_HOST="http://10.77.29.69:8080"
CC_VERSION="/waic/weibox"
CC_VERSION="/waic/samples/detail/id"
CC_INTERFACE="/%s"
# HOST_NAME="http://10.77.29.69:8080/waic/weibox/job?jobKey=%s"
# http://10.77.29.69:8080/master/samples/id/LDA%E6%B5%8B%E8%AF%95%E6%A0%B7%E6%9C%AC
HOST_NAME="%s%s%s" % (CC_HOST, CC_VERSION, CC_INTERFACE)
PARAMS = "?user=%s"
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

def get_args(_sample_key = "", _key = "", _account = ""):
    control_center_job_url = HOST_NAME % _sample_key
    control_center_job_url += PARAMS % _account
    req_json = get(control_center_job_url)
    req_dict = json.loads(req_json) if (
        req_json.startswith("{") or
        req_json.startswith("[") ) else eval(req_json)
    return get_value(_key, req_dict)

def main(_args = []):
    if(len(_args) < 2):
        logger.error("parameter error in python! SAMPLE_KEY,JSON_KEYS")
    _sample_key = _args[1]
    _key = _args[2] if(len(_args) == 3) else "result.data.locations"
    print get_args(_sample_key, _key)
    return 0

if __name__ == '__main__':
    main(sys.argv)
