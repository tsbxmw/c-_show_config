'''
# use urllib2 to get the content of web ; 
# get the version from json data ;
# version : 1.5
# author : mengwei 
# modify : 2017.3.1 - add new function
# modify : 2017.3.2 - add output to file (succesful and fail)
# modify : 2017.3.6 - maybe change the names to one name
# modify : 2017.3.27 - add check the flash wrong build 
# modify : 2017.5.23 - add new check function : when this version can not be downgrade , use this check .
'''
#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import urllib2
import json
import sys
import time
import os

class GetVersion(object):

    def __init__(self,ipadd):
        self.ip = ipadd
        self.content = str()
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_version = "http://" + self.ip + "/service/system/firmware_upgrade/version"
        self.data_login = {'name':'admin', 'pw':'admin111'}
    
    def save_content(self):
        self.session = requests.Session()
        while True:
            try:
                self.session.post(url=self.url_login,data=self.data_login) 
            except:
                print "[getupdateversion-login] waitting for login successfully"
                time.sleep(10)
                continue
            break
        while True:
            try:
                self.content = self.session.get(self.url_version).text
            except:
                print "[getupdateversion-login] waitting for login successfully"
                time.sleep(10)
                continue
            break
        

    def getversion(self):
        while True:
            try:
                self.version = json.loads(self.content)["FWVERSION"]
                return self.version
            except:
                print "[getupdateversion] wrong"
                time.sleep(10)
                continue
            break
        
       

    def splitversion(self):
        self.version_num,self.v_sdp,self.version_date = self.version.split('-')
    
    def compare(self,version_name):
        print "[getupdateversion] firmware version is : " + version_name
        print "[getupdateversion] current  version is : " + self.version_num  + " " + self.version_date
        
        if self.version_date in version_name :
            if self.version_num in version_name:
                print "[getupdateversion][--- update successful (version number and date is right !)--- ]"
                os.system("echo successful > compare")
            else :
                print "[getupdateversion]< error > version number check fail"
                os.system("echo fail > compare")
                sys.exit(1)
                
        else :
            print "[getupdateversion]< error > verison date check fail"
            os.system("echo fail > compare")
            sys.exit(1)
            
        
    def compare_cannotdown(self,version_name):
        print "[getupdateversion-1] not-downgrade version check running"
        print "[getupdateversion-1] before   version is : " + version_name
        print "[getupdateversion-1] current  version is : " + self.version_num + " " + self.version_date
        if self.version_date in version_name :
            if self.version_num in version_name:
                print "[getupdateversion-1][--- update failed (version name and num is right , should not be downgrade !)  ---] "
                os.system("echo fail > compare ")
                sys.exit(1)
            else:
                print "[getupdateversion-1]< successful > version date check OK"
                os.system("echo successful > compare")
                
        else :
            print "[getupdateversion-1]< successful > version date check OK"
            os.system("echo successful > compare")
            

    def  RunCheck(self,version_name):
        try:
            self.save_content()
            self.getversion()
            self.splitversion()
            self.compare(version_name)
        except Exception,e:
            print "[getupdateversion]< error > wrong with error : " + str(e)
            sys.exit(1)
    
    def RunCheck_1(self,version_name):
        try :
            self.save_content()
            self.getversion()
            self.splitversion()
            self.compare_cannotdown(version_name)
        except Exception,e:
            print "[getupdateversion-1]< error > wrong with error : " + str(e)
            sys.exit(1)
# sdp_edison.2.2.1_rtm.20170301.bin
# 2.2.1_rtm-sdp-20170301
