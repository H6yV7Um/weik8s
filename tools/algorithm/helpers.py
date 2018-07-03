# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/5.
import json,sys,os
import urllib,urllib2

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

#POST：
def post(_url,
         _values):
    try:
        data = urllib.urlencode(_values)    #适用urllib对数据进行格式化编码
        logger.debug("URL : " + _url)    #输出查看编码后的数据格式
        logger.debug("DATA : " + data)    #输出查看编码后的数据格式
        req = urllib2.Request(_url, data)    #生成页面请求的完整数据
        response = urllib2.urlopen(req)     #发送页面请求
        req_info = response.read()
        logger.debug(req_info)
        return req_info
    except (urllib2.HTTPError, Exception),e:
        logger.error(e)
        exit(1)
    return req_info    #获取服务器返回的页面信息


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
            tail_dict = tail_dict[0] if len(tail_dict)>0 else None
        tmp_obj = get_value(_key_path[point_idx+1:], tail_dict)
        # return tmp_obj if (not isinstance(tmp_obj, list)) else tmp_obj[0]
    # else:
    #     return tmp_obj
    return tmp_obj

def sys_run(_cmd = ''):
    logger.info("command running... ")
    logger.debug("command running... %s" % _cmd)
    response_code = os.system(_cmd)
    if(response_code != 0):
        logger.error("run command %s found error!! with exit code %d!!" % (_cmd,response_code))
    else:
        logger.info("run command success!! with exit code %d!!" % response_code)
        logger.debug("run command %s success!! with exit code %d!!" % (_cmd, response_code))
    return response_code

def job_space(_job_key = ""):
    return os.path.abspath(os.path.dirname(__file__) + "../../ksp/%s" % _job_key)

