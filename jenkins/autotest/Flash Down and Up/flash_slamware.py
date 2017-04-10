#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng @ slamtec.inc
date : 2017.03.10
version : 1.1
modify : 20170407 - add the up down to the summary.html
'''

import sys
import os
import time
import json
from Flash import Flash
from Getfiles import Getfiles
from Update import Update
from Checkversion import GetVersion
from datetime import datetime
from createreport import Report
from debugmode import Root


if __name__ == "__main__":

    try:
        envipadd = "IP_SLAMWARE"
        envupname = "NAME_OF_UPBUILD"
        envdownname = "NAME_OF_DOWNBUILD"
        envcount = "COUNT_OF_DOWNUP"
        envproductname = "TEST_NAME"
        localupdir = "up"
        localdowndir = "down"
        
        localuppath = "..\\testdata\\sdprprom\\" + localupdir
        localdownpath = "..\\testdata\\sdprprom\\" + localdowndir

        testinfo = []
        
        flash = Flash()
        fileuppath = flash.getEnv(envupname)
        filedownpath = flash.getEnv(envdownname)
        count = flash.getEnv(envcount)
        ipadd = flash.getEnv(envipadd)
        productname = flash.getEnv(envproductname)

        fileupname = flash.getFileName(fileuppath)
        filedownname = flash.getFileName(filedownpath)
        print "[down&up] up name : " + str(fileupname )
        print "[down&up] down name : " + str(filedownname)

        getfile = Getfiles()
        getfile.Getfile(fileuppath,localuppath)
        getfile.Getfile(filedownpath,localdownpath)
        
        updateup = Update(ipadd,localuppath+"\\"+fileupname)
        updatedown = Update(ipadd,localdownpath+"\\"+filedownname)
        check = GetVersion(ipadd)
        
        jsoninfo = {}
        jsoninfo["time"] = "0"
        jsoninfo["values"] = "0"
        jsoninfo["count"] = str(count)
        testinfo.append(jsoninfo)
        
        
        print ("******************************************************************")
        print ("[Flash down&up] ALL :" + str(count))
        i = 1
        while i < (int(count) + 1):
            print ("----------------[time %s]----------------"%(i))
            print ("[Flash down] start up now ...")
            jsoninfo = {}
            infos = {}
            jsoninfo["time"] = str(i)
            check.save_content()
            version_before = check.getversion()
            infos["version_down_before"] = str(version_before)
            infos["version_down_file"] = str(filedownname)
            infos["remote_down_path"] = str(filedownpath)
            begindown = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()) )
            infos["down_begin"] = str(begindown)
            time_use1 = datetime.now()
            #-----------------------up is info ---------#
            updatedown.RunUpdate()
            check.RunCheck(filedownname)
            #-----------------------up is downgrade ----------#
            check.save_content()
            version_after = check.getversion()
            infos["version_down_after"] = str(version_after)
            time_use2 = datetime.now()
            infos["down_timeuse"] = str((time_use2-time_use1).seconds)
            enddown = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
            infos["down_end"] = str(enddown)
            jsoninfo["down_values"] = infos
            print ("[getlog] now ....")
            logroot = Root(ipadd)
            logroot.Run("root-log","logdown"+str(i)+".log")
            print ("******************")
            print ("=====================")
            print ("[Flash up] start up now ...")
            
            infos = {}
            check.save_content()
            version_before = check.getversion()
            infos["version_up_before"] = str(version_before)
            infos["version_up_file"] = str(fileupname)
            infos["remote_up_path"] = str(fileuppath)
            beginup = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()) )
            infos["up_begin"] = str(beginup)
            time_use1 = datetime.now()
            #-----------------------up is info ---------#
            updateup.RunUpdate()
            check.RunCheck(fileupname)
            #-----------------------up is upgrade ----------#
            check.save_content()
            version_after = check.getversion()
            infos["version_up_after"] = str(version_after)
            time_use2 = datetime.now()
            infos["up_timeuse"] = str((time_use2-time_use1).seconds)
            endup = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
            infos["up_end"] = str(endup)
            jsoninfo["up_values"] = infos
            testinfo.append(jsoninfo)
            print ("[getlog] now ....")
            logroot = Root(ipadd)
            logroot.Run("root-log","logup"+str(i)+".log")
            print ("******************")
            i = i + 1
        
        output = open('testinfo.json', 'wb')
        output.write(json.dumps(testinfo))
        output.close()
        report = Report("Flash Down and Up")
        report.runCreateDownUpBuildReport(ipadd,productname)

    except Exception,e:
        print ("wrong with ??" + str(e))
