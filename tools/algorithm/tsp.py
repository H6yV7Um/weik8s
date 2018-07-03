# !/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
def job_space(_job_key = ""):
    return os.path.abspath(os.path.dirname(__file__) + "../../ksp/%s" % _job_key)

if __name__ == '__main__':
    print job_space(sys.argv[1])


