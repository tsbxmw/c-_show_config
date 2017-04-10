#!/usr/bin/python
# -*- coding:utf-8 -*-

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
        self.firmware_path = fm_path
        self.data_login = {'name':'admin', 'pw':'admin111'}


    def Login(self):
        self.session = requests.Session()
        print '[login] session init, ready to login' 
        login = self.session.post(url=self.url_login,data=self.data_login)
        print '[login] ok'
        return login

    def Update(self):
        try:
            files = {'file': open(self.firmware_path, 'rb')}
            print '[update] load firmware file successfully, ready to upload firmware file'
            startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print '[ start time ] ' + str(startupdate) 
            self.session.post(url=self.url_update,files=files)
            print ('[update] wait for update [120s]')
            time.sleep(120)
        except:
            print ('[update] wait for update [120s]')
            time.sleep(120)
        
        

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
    #except:
     #   print 'upload firmware file successfully, wait for updating'
     #   print sys.exc_info()
