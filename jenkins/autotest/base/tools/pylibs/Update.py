#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
# version : v1.22
# authore : wei.meng @ slamtec.com
# date    : 20170304
# modify  : 20170503 - add update_new and runupdate_new function at the new slamware version 2.4.0_dev
# modify  : 20170518 - /service/system/system_upgrade is the new action url.
# modify  : 20170605 - bug fix , but not work.

####
#   ip - slamware ip
#   url_login - login action url
#   url_update - update action url of version 2.3.x and before
#   url_update_new - updateaction url of version 2.4.x and new
####
'''


import requests
import json
import sys,os
import time
import subprocess,traceback,platform

class Update(object):

    def __init__(self,ipadd,fm_path):
        self.ip = ipadd
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_update = 'http://' + self.ip + '/service/system/firmware_upgrade/full_update'
        self.url_status = 'http://' + self.ip + '/service/system/task/status'
        self.url_update_new = 'http://' + self.ip + '/service/system/system_upgrade'
        self.url_restore = 'http://' + self.ip + '/service/system/restore'
        self.firmware_path = fm_path
        self.data_login = {'name':'admin', 'pw':'admin111'}

    # Login the slamware web Administrator with 'admin' and 'admin111'
    def Login(self):
        self.session = requests.Session()
        print '[login] session init, ready to login' 
        login = self.session.post(url=self.url_login,data=self.data_login)
        print '[login] ok'
        return login

    # Update : using file upload the firmware and run it
    def Update(self):
        try:
            files = {'file': open(self.firmware_path, 'rb')}
            print '[update] load firmware file successfully, ready to upload firmware file'
            startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print '[ start time ] ' + str(startupdate) 
            self.session.post(url=self.url_update,files=files)
            print ('[update] wait for update [240 s]')
            time.sleep(240)
        except Exception,e:
            if "BadStatusLine" in str(e):
                print "[update] <exception> " + str(e)       
                time.sleep(240)        
            else:
                print "[update] <error> " + str(e)
                time.sleep(10)
                print "[update] try again ..."
                self.Update()


    # do not work fine , when "bad line" issue coming , the expect always do the failed job .
    def Update_1(self):
        while True:
            try:
                files = {'file': open(self.firmware_path, 'rb')}
                print '[update] load firmware file successfully, ready to upload firmware file'
                startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print '[ start time ] ' + str(startupdate) 
                self.session.post(url=self.url_update,files=files)
                print ('[update] wait for update [240 s]')
                time.sleep(240)
                break
            except Exception,e:
                print "[update] <error> " + str(e)
                time.sleep(2)
                continue
            except:
                print "[update] <error> wrong with update"
                time.sleep(2)
                continue


    # using for the new version check , 2.4.0_dev and higher would be work fine
    def Update_New(self):
        try:
            files = {'file':open(self.firmware_path,'rb')}
            print '[update_new] load the firmware file '
            startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print '[update_new - start time] ' + str(startupdate)
            self.session.post(url=self.url_update_new,files=files)
            print '[update_new] wait for update [240 s]'
            time.sleep(240)
        except Exception,e:
            if "BadStatusLine" in str(e):
                print "[update] <exception> " + str(e)       
                time.sleep(240)        
            else:
                print "[update] <error> " + str(e)
                time.sleep(10)
                print "[update] try again ..."
                self.Update()

    # try to fix some bad line issue , but not work fine ,would fix it on new deal.
    def Update_New_1(self):
        while True:
            try:
                files = {'file':open(self.firmware_path,'rb')}
                print '[update_new] load the firmware file '
                startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print '[update_new - start time] ' + str(startupdate)
                self.session.post(url=self.url_update_new,files=files)
                print '[update_new] wait for update [240 s]'
                time.sleep(240)
                break
            except Exception,e:
                print "[Update-new] <error> wrong with " + str(e)
                time.sleep(2)
                continue
            except:
                print "[Update-new] <error> wrong with update"         
                time.sleep(2)
                continue
    
    def GetResult(self):
        while True:
            if self.Ping():
                print("[ping] ok")
            else:
                print("[ping] waitting for update complete")
                time.sleep(30)
                continue
            try:
                self.Login().raise_for_status() 
            except:
                print "[login] waitting for update complete"
                time.sleep(10)
                continue
            try:
                req = self.session.get(url=self.url_status)
                req.raise_for_status() 
            except :
                print "[update] waitting for update complete"
                time.sleep(10)
                continue
            ### first of all , using the web info to judge the update complete or not ,
            ### but now ,sdk connect and version info is the double check
            # req_json = json.loads(req.text)
            # if req_json['message'] == 'Idle':
                # endupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print '[ end time ] ' + str(endupdate) 
                # print 'update successfully'
                # break
            os.system("sdkconnect.exe " + self.ip)
            file = open("connect.result","r")
            f = file.readline()
            file.close()
            
            if "successful" in f:
                print "[sdk-connect] core startup successful"
                break
            else :
                time.sleep(30)
                    
                
    def Ping(self):
        cmd = 'ping -n %d %s'%(1,self.ip)
        try:
            p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (stdoutput,erroutput) = p.communicate()
        except Exception, e:
            traceback.print_exc()
        return stdoutput.find('TTL')>=0        

    def RunUpdate(self):
        try:
            i = 1
            while True: 
                print ("[update] try " + "times " + str(i))
                if self.Ping():
                    print("[ping] ok")
                else:
                    print("[ping] waitting for network online")
                    time.sleep(30)
                    i = i + 1
                    continue
                try:
                    self.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successfully"
                    time.sleep(10)
                    i = i + 1
                    continue
                break

            self.Update()
            self.GetResult()

        except requests.exceptions.ConnectionError:
            print 'requests.exceptions.ConnectionError'
            sys.exit(1)
        except requests.exceptions.Timeout:
            print 'requests.exceptions.Timeout'
            sys.exit(1)
        except requests.exceptions.RequestException:
            print 'requests error'
            sys.exit(1)
            
    def RunUpdate_New(self):
        try:
            i = 1
            while True:
                print ("[update_new] try times " + str(i))
                if self.Ping():
                    print ("[update_new][ping] ok")
                else :
                    print ("[update_new][ping] waiting for network online")
                    time.sleep(30)
                    i = i + 1
                    continue
                try:
                    self.Login().raise_for_status()
                except:
                    print ("[update_new][login] waitting for login successfully")
                    time.sleep(10)
                    i = i + 1
                    continue
                break   

            self.Update_New()
            self.GetResult()
        
        

                
        
        except requests.exceptions.ConnectionError:
            print 'requests.exceptions.ConnectionError'
            sys.exit(1)
        except requests.exceptions.Timeout:
            print 'requests.exceptions.Timeout'
            sys.exit(1)
        except requests.exceptions.RequestException:
            print 'requests error'
            sys.exit(1)
                    
                
    #except:
     #   print 'upload firmware file successfully, wait for updating'
     #   print sys.exc_info()
