#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng @ slamtec.inc
date : 2017.03.09
version : 1.3
modify : 20170420 - add run the script remove_version.sh
modify : 20170421 - remove the run of the remove_version.sh
'''

import sys
import os
import time
import json
from Flash import Flash
from Getfiles import Getfiles
from Update import Update
from createreport import Report
from Checkversion import GetVersion
from datetime import datetime
from debugmode import Root
from SSH import Ssh,Sftp


if __name__ == "__main__":

    try:
        envipadd = "IP_SLAMWARE"
        envname = "NAME_OF_ONEBUILD"
        envcount = "COUNT_OF_ONEBUILD"
        envproductname = "TEST_NAME"
        localdir = "oneday"
        localpath = "..\\testdata\\sdprprom\\" + localdir

        testinfo = []
        output = open('testinfo.json', 'wb')
        
        flash = Flash()
        filepath = flash.getEnv(envname)
        count = flash.getEnv(envcount)
        ipadd = flash.getEnv(envipadd)
        productname = flash.getEnv(envproductname)
        
        filename = flash.getFileName(filepath)
        print filename

        getfile = Getfiles()
        getfile.Getfile(filepath,localpath)
        
        update = Update(ipadd,localpath+"\\"+filename)
        check = GetVersion(ipadd)
        
        jsoninfo = {}
        jsoninfo["time"] = "0"
        jsoninfo["values"] = "0"
        jsoninfo["count"] = str(count)
        testinfo.append(jsoninfo)
        
        print ("******************************************************************")
        print ("[Flash] ALL :" + str(count))
        i = 1
        while i < (int(count) + 1):
            print ("----------------[time %s]----------------"%(i))
            print ("[Flash] start up now ...")
            # remove the run ssh stage
            '''rmversion = Ssh(ipadd,"root","slamware123")
            rmversion.Connect()
            rmversion.Exec("chmod a+x remove_version.sh")
            rmversion.Exec("./remove_version.sh")
            rmversion.Close()'''
            jsoninfo = {}
            infos = {}
            jsoninfo["time"] = str(i)
            check.save_content()
            version_before = check.getversion()
            infos["version_before"] = str(version_before)
            infos["version_file"] = str(filename)
            infos["remote_path"] = str(filepath)
            beginupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()) )
            infos["begin"] = str(beginupdate)
            time_use1 = datetime.now()
            update.RunUpdate()
            check.RunCheck(filename)
            infos["version_before"] = str(version_before)
            time_use2 = datetime.now()
            infos["timeuse"] = str((time_use2-time_use1).seconds)
            endupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
            infos["end"] = str(endupdate)
            check.save_content()
            version_after = check.getversion()
            infos["version_after"] = str(version_after)
            jsoninfo["values"] = infos
            testinfo.append(jsoninfo)
            
            print ("[getlog] now ....")
            logroot = Root(ipadd)
            logroot.Run("root-log","log"+str(i)+".log")
            print ("******************")
            '''print ("[getrealsense] log ... ")
            logroot.TestRealSense()
            file = open(".\\realsense.log",'r')
            linef = file.readline()
            file.close()
            if "Successfully" in linef :
                print "[testrealsense] successful"
            else:
                print "[testrealsense] fail - realsense not start !"
                sys.exit(1)'''
            i = i + 1
        output.write(json.dumps(testinfo))    
        output.close()
        print ("[Flash] all test end now ...")
        print ("******************************************************************")
        report = Report("Flash One Build")
        report.runCreateOneBuildReport(ipadd,productname)


    except Exception,e:
        print ("wrong with ??" + str(e))
