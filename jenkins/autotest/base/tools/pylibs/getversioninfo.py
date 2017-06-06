#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
# version : 1.0
# date    : 20170531
# author  : wei.meng @ slamtec.com
# description -  using to read the version-limit file and return the limit version-limit
#
'''

'''
{
"current":"2.4.0_dev",
"min_down":"2.1.2_rtm_20170212",
"no_max_down":"2.1.3_rtm_20170311",
"max_up":"2.4.1_rtm_20170425",
"no_min_up":"2.4.2_dev_20170525"
}
min_down is downgrade version name
max_up is upgrade version name
no_max_down is the wrong version name
'''

import os,sys,time
import json


reload(sys)
sys.setdefaultencoding( "utf-8")

class Gvinfo(object):
    def __init__(self):
        print ("[Gvinfo] init")
        self.versioninfo = {}

    def openfile(self,configfile):
        try:
            fp = open(configfile,'r')
            self.json_versioninfo = json.load(fp)
            fp.close()
        except Exception,e:
            print ("[openfile] error with " + str(e))

    def getversion(self,currentversion):
        for info in self.json_versioninfo:
            if info["current"] in currentversion :
                self.versioninfo = info
                break

    def getdownversion(self):
        return self.versioninfo["min_down"]

    def getupversion(self):
        return self.versioninfo["max_up"]

    def getwrongversion(self):
        return self.versioninfo["no_min_up"]
        
        
        
        
        