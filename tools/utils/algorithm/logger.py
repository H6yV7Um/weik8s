# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2017/12/11.

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


