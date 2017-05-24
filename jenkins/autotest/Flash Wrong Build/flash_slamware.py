#!/usr/bin/python
# -*- coding:utf-8 -*-


'''
# author : wei.meng @ slamtec.inc
# date : 2017.03.09
# version : 1.1
# modify : 2017.05.24 - add 2.4 version check before update
'''

import sys
import os
import time
import json
from Flash import Flash
from Getfiles import Getfiles
from Update import Update
from Checkversion import GetVersion
from createreport import Report
from datetime import datetime
from debugmode import Root

if __name__ == "__main__":

    try:
        envipadd = "IP_SLAMWARE"
        envname = "NAME_OF_WRONGBUILD"
        envproductname = "TEST_NAME"
        localdir = "wrong"
        localpath = "..\\testdata\\sdprprom\\" + localdir
        
        jsoninfo = {}
        output = open('testinfo.json', 'wb')
        
        flash = Flash()
        filepath = flash.getEnv(envname)
        ipadd = flash.getEnv(envipadd)
        productname = flash.getEnv(envproductname)

        
        filename = flash.getFileName(filepath)
        print filename

        getfile = Getfiles()
        getfile.Getfile(filepath,localpath)

        update = Update(ipadd,localpath+"\\"+filename)
        check = GetVersion(ipadd)
        check.save_content()
		thisversion = str(check.getversion())
        jsoninfo["version_before"] = thisversion
        jsoninfo["version_file"] = str(filename)
        jsoninfo["remote_path"] = str(filepath)
        print ("******************************************************************")
        print ("[Flash] start up now ...")
        beginupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()) )
        jsoninfo["begin"] = str(beginupdate)
        time_use1 = datetime.now()
		if '2.4' in thisversion:
			update.RunUpdate_New()
		else:
			update.RunUpdate()
			
        time_use2 = datetime.now()
        jsoninfo["timeuse"] = str((time_use2-time_use1).seconds)
        endupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
        jsoninfo["end"] = str(endupdate)
        check.save_content()
        version_after = check.getversion()
        check.RunCheck_1(version_after)
        output.write(json.dumps(jsoninfo))
        output.close()
        
        print ("[Flash] update end now ...")
        print ("******************************************************************")
        print ("[getlog] now ....")
        logroot = Root(ipadd)
        logroot.Run("root-log","system.log")
        print ("******************")
        report = Report("Flash Wrong Build")
        print ipadd
        print productname
        report.runCreateReport(ipadd,productname)
    except Exception,e:
        print ("wrong with ??" + str(e))
