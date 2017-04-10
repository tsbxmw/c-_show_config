#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng @ slamtec.inc
date : 2017.03.09
version : 1.0
'''
import sys
import os
import time


class Flash(object):
    def __init__(self):
        print "[Flash]"

    def fileExist(self,filepath):
        return os.path.exists(filepath)

    def getEnv(self,envname):
        return os.getenv(envname)

    def getFileName(self,filepath):
        filename=None
        for x in filepath.split("\\"):
            filename = x
        return filename


if __name__ == "__main__":

    try:

        envname = "NAME_OF_ONEBUILD"
        flash = Flash()
        filepath = flash.getEnv(envname)
        filename = flash.getFileName(filepath)
        print filename
    except:
        print ("wrong with ??")
