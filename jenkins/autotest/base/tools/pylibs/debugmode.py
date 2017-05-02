#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
# before : pip install requests 
   it is useful to the zeus-edison device to get into debug and simulator mode
   if u want to use to sdp , change the Simulator's  
            ssh.Exec("mv /etc/sdp_ref_rplidar.json /home/root/sdp_ref.json ")
            ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref_rplidar.json ")
    to:
            ssh.Exec("mv /etc/sdp_ref.json /home/root/sdp_ref.json ")
            ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref.json ")
# author : slamtec.inc - wei.meng
# date   : 20170301
# modify : 2017.03.02 - add info of data , change user_pass to self.unlock_info
# modify : 2017.03.03 - change to root mode , delete the simulator mode
# modify : 2017.03.09 - add new flag root 
# modify : 2017.03.17 - add new flag unroot , log , unsimulator -- add new function getlog
# modify : 2017.04.20 - add new function : test the depthcam
'''

import requests
import json
import sys,os
import time
import traceback,platform
from SSH import Ssh,Sftp

class Root(object):

    def __init__(self,ipadd):
        self.ip = ipadd
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_debug = 'http://' + self.ip + '/service/system/admin/challenge'
        self.url_unroot = 'http://' + self.ip + '/service/system/admin/unroot'
        self.url_sn = 'http://' + self.ip + '/service/system/admin/sn'
        self.url_version = "http://" + self.ip + "/service/system/firmware_upgrade/version"
        self.data_login = {'name':'admin', 'pw':'admin111'}
        self.ssh_user = "root"
        self.ssh_pass = "slamware123"
        self.unlock_info={'ip':'10.8.2.160','user':'token','pass':'admin123'}
        self.data_debug = None


    def Login(self):
        print "the ip is " + self.ip
        self.session = requests.Session()
        print '[Login] session init, ready to login.' 
        login = self.session.post(url=self.url_login,data=self.data_login)
        print '[Login] login successfully'
        return login

    
    def GetSN(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.sn = json.loads(self.content)["DeviceSN"]
            print "[getdevicesn] sn is " + self.sn
            return self.sn
        except:
            print ('[device sn] wrong with get sn')
            
    def GetSN_1(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.sn_1 = json.loads(self.content)["S/N"]
            print "[getsn] sn is " + self.sn_1
            return self.sn_1
        except:
            print ('[sn] wrong with get sn')

    def GetIpMode(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.ipmode = json.loads(self.content)["MODE : SSID : IP"]
            print "[getip] ip is " + self.ipmode
            return self.ipmode
        except:
            print ('[getip] wrong with get sn')
       

    def Getversion(self):
        self.content = self.session.get(self.url_version).text
        self.version = json.loads(self.content)["FWVERSION"]
        print self.version
        return self.version


    def GetUnlock(self):
        try:
            ssh = Ssh(self.unlock_info['ip'],self.unlock_info['user'],self.unlock_info['pass'])
            ssh.Connect()
            self.snunlock = ssh.Exec("cd unlock && ./gen_challenge_token.sh " + self.sn)[2]
            ssh.Close()
            print "[sn-unlock-num] " + self.snunlock
            self.data_debug = {'cha-token':self.snunlock}
        except:
            print ('[sn-unlock] wrong with get sn unlock')

    def Root(self):
        try:
            self.session.post(url=self.url_debug,data=self.data_debug)
            print "[root] successful"
            return True
        except:
            print ('[root] wrong with root')
            return False
            
    def UnRoot(self):
        try:
            self.session.post(url=self.url_unroot)
            print "[unroot] successful"
        except:
            print ('[unroot] wrong with the unroot')

    def UploadFile(self):
        try:
            sf = Sftp(self.ip)
            sf.Connect()
            sf.PutFile("..\\testdata\\mapjson\\5f.bmp","/home/root/5f.bmp")
            sf.PutFile("..\\testdata\\mapjson\\sdp_ref_simulator.json","/home/root/sdp_ref_simulator.json")
            sf.Close()
            print "[upload-file] successful"
        except:
            print ('[upload file] wrong with the it')

    def Simulator(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("mv /etc/sdp_ref_rplidar.json /home/root/sdp_ref.json ")
            ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref_rplidar.json ")
            ssh.Exec("reboot -n")            
            ssh.Close()
            print "[Simulator Mode] switch successful"
        except:
            print ('[Simulator Mode]Simulator Mode wrong ')

            
    def TestRealSense(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("chmod a+x open.sh")
            ssh.Exec("./open.sh | grep Successfully > realsense.log")
            ssh.Close()
            
            sf = Sftp(self.ip)
            sf.Connect()
            sf.GetFile("/home/root/realsense.log",".\\realsense.log")
            sf.Close()
            print "[Test Realsense] - successful "
        except:
            print "[Test Realsense] - fail to "
            
            
    def UnSimulator(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("mv /etc/sdp_ref_rplidar.json /home/root/sdp_ref_simulator.json ")
            ssh.Exec("mv /home/root/sdp_ref.json /etc/sdp_ref_rplidar.json ")
            ssh.Exec("reboot -n")            
            ssh.Close()
            print "[Simulator Mode] switch successful"
        except:
            print ('[UnSimulator] wrong')
    
    def GetLog(self,logname):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("journalctl > /home/root/system.log")          
            ssh.Close()
            print ("[getlog] start get log")
            sf = Sftp(self.ip)
            sf.Connect()
            sf.GetFile("/home/root/system.log","log\\"+logname)            
            sf.Close()
            print "[getlog] switch successful"
        except:
            print ('[UnSimulator] wrong')
            
            
    def Run(self,flag,logname):
        try:                
            i = 1
            if "root" in flag :
                while True: 
                    print ("try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        print "[login] waitting for login successful"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.GetSN() 
                    except:
                        print "[GetSN] GetSN wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.GetUnlock()
                    except:
                        print "[GetUnlock] GetUnlock wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if self.Root():
                            print "root ok"
                        else:
                            print "[Root] Root wrong"
                            time.sleep(10)
                            i = i + 1
                            continue
                    except:
                        print "[Root] Root wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if "log" in flag:
                            print("--------")
                            self.GetLog(logname)
                        #root.UploadFile() 
                    except:
                        print "[GetLog] GetLog wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                        
                    try:
                        if "simulator" in flag:
                            print("--------")
                            self.UploadFile() 
                        
                    except:
                        print "[UploadFile] UploadFile wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if "simulator" in flag:
                            self.Simulator()
                            print("--------")
                       
                    except:
                        print "[Simulator] Simulator wrong"
                        time.sleep(10)
                        i = i + 1
                        continue
                   
                    break
            if "unroot" in flag:
                while True: 
                    print ("try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        print "[login] waitting for login successful"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.UnRoot()
                    except:
                        print ("[unroot] waitting for unroot successful")
                        i = i + 1
                        continue
                    break
                    try:
                        self.UnRoot()
                    except:
                        print ("[unroot] waitting for unroot successful")
                        i = i + 1
                        continue
                    break
            if "unsimulator" in flag :
                while True: 
                    print ("try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        print "[login] waitting for login successful"
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.UnSimulator()
                    except:
                        print ("[UnSimulator] waitting for UnSimulator successful")
                        i = i + 1
                        continue
                    break
                    
        except requests.exceptions.ConnectionError:
            print 'requests.exceptions.ConnectionError'
            sys.exit(1)
        except requests.exceptions.Timeout:
            print 'requests.exceptions.Timeout'
            sys.exit(1)
        except requests.exceptions.RequestException:
            print 'requests error'
            sys.exit(1)
        
if __name__ == "__main__":
    try:
        args = sys.argv
        if len(args) < 3:
            print "[debugmode.py] wrong with the argv"
        ipadd = args[1]
        flag = args[2]
        
        root = Root(ipadd)
                    
        i = 1
        if "root" in flag :
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.GetSN() 
                except:
                    print "[GetSN] GetSN wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.GetUnlock()
                except:
                    print "[GetUnlock] GetUnlock wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.Root()
                    print "root ok"
                except:
                    print "[Root] Root wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    if "log" in flag:
                        print("--------")
                        root.GetLog()
                    #root.UploadFile() 
                except:
                    print "[GetLog] GetLog wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                    
                try:
                    if "simulator" in flag:
                        print("--------")
                        root.UploadFile() 
                    
                except:
                    print "[UploadFile] UploadFile wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    if "simulator" in flag:
                        root.Simulator()
                        print("--------")
                   
                except:
                    print "[Simulator] Simulator wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
               
                break
        if "unroot" in flag:
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.UnRoot()
                except:
                    print ("[unroot] waitting for unroot successful")
                    i = i + 1
                    continue
                break
                try:
                    root.UnRoot()
                except:
                    print ("[unroot] waitting for unroot successful")
                    i = i + 1
                    continue
                break
        if "unsimulator" in flag :
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.UnSimulator()
                except:
                    print ("[UnSimulator] waitting for UnSimulator successful")
                    i = i + 1
                    continue
                break
                
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
