# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/5.
import json
import os
import urllib
import urllib2

import weibox_macros
from logger import logger


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

#POST_BASE：
def post_base(_url,
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
    return req_info    #获取服务器返回的页面信息

#POST：
def post_json(_url,
         _values):
    try:
        headers = {'Content-Type': 'application/json'}
        if(not _values.has_key("body")):
            raise IOError("url data encode when post json data. because of cannot found json body")
        json_assert = json.loads(_values.get("body"))
        data = _values.get("body")
        param_value = _values.copy()
        param_value.pop("body")
        if(len(param_value) > 0):
            param = urllib.urlencode(param_value)
            _url += ("?" + param)
        logger.debug("URL : " + _url)    #输出查看编码后的数据格式
        logger.debug("DATA : " + data)    #输出查看编码后的数据格式
        req = urllib2.Request(url=_url, data=data, headers=headers)    #生成页面请求的完整数据
        response = urllib2.urlopen(req)     #发送页面请求
        req_info = response.read()
        logger.debug(req_info)
        return req_info
    except (urllib2.HTTPError, Exception),e:
        logger.error(e)
    return req_info    #获取服务器返回的页面信息

#POST：
def post_file(_url,
              _values):
    try:
        headers = {'Content-Type': 'application/json'}
        if(not _values.has_key("file")):
            raise IOError("url data encode when post json data. because of cannot found json body")
        param_value = _values.copy()
        file_name = param_value.pop("file")
        file_path = os.path.abspath(file_name)
        file_reader = open(file_path,"r")
        file_content = file_reader.read()
        param_value["stdout"] = file_content
        if(len(param_value) > 0): 
            param = urllib.urlencode(param_value) 
            # _url += ("?" + param)
        logger.debug("URL : " + _url)    #输出查看编码后的数据格式
        logger.debug("DATA : " + file_content)    #输出查看编码后的数据格式
        req = urllib2.Request(url=_url, data=param, headers=headers)    #生成页面请求的完整数据
        response = urllib2.urlopen(req)     #发送页面请求
        req_info = response.read()
        logger.debug(req_info)
        return req_info
    except (urllib2.HTTPError, Exception),e:
        logger.error(e)
    return req_info    #获取服务器返回的页面信息

#POST：
def post_stdout(_url,
              _values):
    try:
        if(not _values.has_key("file")):
            raise IOError("url data encode when post json data. because of cannot found json body")
        param_value = _values.copy()
        file_name = param_value.pop("file")
        file_path = os.path.abspath(file_name)
        file_reader = open(file_path,"r")
        file_content = file_reader.read()
        param_value["stdout"] = file_content
        return post_base(_url=_url, _values = param_value)
    except Exception,e:
        logger.error(e.message)


def post(_url, _values, _data_type = "json"):
    if(_data_type == "json"):
        return post_json(_url, _values)
    elif(_data_type == "file"):
    #     TODO: post a file to target interface
        return post_file(_url, _values)
    elif(_data_type == "stdout"):
        return post_stdout(_url, _values)
    else:
        return post_base(_url, _values)

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

def sys_popen(_cmd = ''):
    logger.info("command running... ")
    logger.debug("command running... %s" % _cmd)
    output = os.popen(_cmd).read()
    return output


def job_space(_job_key = ""):
    # dir path need to be weibox/tools/utils/
    # workspace need to be weibox/ksp/${JOB_KEY}/
    return os.path.abspath(weibox_macros.job_util_path() + "/../../ksp/%s" % _job_key)

def job_key_check(_job_key = "", _func_name = "", _file_name = ""):
    if(_job_key == None):
        logger.error("_job_key Found None when " + "[= %s =] in [@ %s @] " % (_func_name, _file_name))
    if(len(_job_key)<1):
        logger.error("_job_key Found EMPTY when " + "[= %s =] in [@ %s @] " % (_func_name, _file_name))

