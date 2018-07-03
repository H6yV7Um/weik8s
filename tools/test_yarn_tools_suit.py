# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by enzhao on 2018/1/22. 

import random, unittest, sys
import job_submit

class Test_yarn_tools_suit(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)
        print "[= %s =] passed for test in [@ %s @] " % (sys._getframe().f_code.co_name,  __name__.upper())

    def test_read_yarn_app_id(self):
        args = ['-c', 'user:', 'feed_weibo', 'Exception', 'in', 'thread', 'main', 'org.apache.spark.SparkException:', 'Application', 'application_1505098678619_13322', 'finished', 'with', 'failed', 'status', 'at', 'org.apache.spark.deploy.yarn.Client.run(Client.scala:1132)', 'at', 'org.apache.spark.deploy.yarn.Client$.main(Client.scala:1178)', 'at', 'org.apache.spark.deploy.yarn.Client.main(Client.scala)', 'at', 'sun.reflect.NativeMethodAccessorImpl.invoke0(Native', 'Method)', 'at', 'sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)', 'at', 'sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)', 'at', 'java.lang.reflect.Method.invoke(Method.java:498)', 'at', 'org.apache.spark.deploy.SparkSubmit$.org$apache$spark$deploy$SparkSubmit$$runMain(SparkSubmit.scala:736)', 'at', 'org.apache.spark.deploy.SparkSubmit$.doRunMain$1(SparkSubmit.scala:185)', 'at', 'org.apache.spark.deploy.SparkSubmit$.submit(SparkSubmit.scala:210)', 'at', 'org.apache.spark.deploy.SparkSubmit$.main(SparkSubmit.scala:124)', 'at', 'org.apache.spark.deploy.SparkSubmit.main(SparkSubmit.scala)', '18/01/22', '16:24:41', 'INFO', 'util.ShutdownHookManager:', 'Shutdown', 'hook', 'called', '18/01/22', '16:24:41', 'INFO', 'util.ShutdownHookManager:', 'Deleting', 'directory', '/tmp/spark-25c7911d-8d38-4696-87cc-a5dc7bfa1fbc']
        # read_yarn_app_id.resolve_yarn_app_id(args)
        # job_submit.job_submit(_job_key="enzhao-dataflow-demo-001-7-35505310406646016")
        # job_submit.job_submit(_job_key="enzhao-emr-cluster-submit-027-cron-01-3-35505510028973824")
        job_submit.job_submit(_job_key="enzhao-emr-cluster-submit-028-41-35505757479881216")
        print "[= %s =] passed for test in [@ %s @] " % (sys._getframe().f_code.co_name,  __name__.upper())
        # assert len(cluster_rst[2]) == 5
        # assert len(algorithm_rst[2]) == 2

