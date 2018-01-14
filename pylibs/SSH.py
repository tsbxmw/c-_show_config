#-*- coding: utf-8 -*-
#!/usr/bin/python 

'''
# version : 1.4
# attention ：using paramiko module --- using 'pip install paramiko' to install the module
# functon : ssh and sftp function
# author : mengwei
# date : 2017.03.01
# modify : -add Sftp module to transport the file
# modify : 2017.03.02 - change the Ssh() to Ssh(ip,user,pass)
# modify : 2017.03.09 - change to the module
# modify : 2017.03.17 - add new function getfile
# modify : 2017.05.25 - add new function Exec_noreturn , try to run the 'reboo' command, but not work fine
'''

import paramiko
import sys
import time
from LogShow import LogShow

class Ssh(object):
    def __init__(self,ipadd,username,password):
        self.ip = ipadd
        self.username = username
        self.password = password
        self.ls = LogShow("SSH")

    def Connect(self):
        try:
            self.connect = paramiko.SSHClient()
            self.connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connect.connect(self.ip,22,self.username,self.password,timeout=5)
        except Exception,e:
            self.ls.log_print("system","[SSH Connect] : wrong with it -- " + str(e))

    def Exec(self,cmd):
        try:
            self.ls.log_print("system","[exec] " + str(cmd))
            stdin, stdout, stderr = self.connect.exec_command(cmd)
            out = stdout.readlines()
            return out
        except Exception,e:
            self.ls.log_print("system","[SSH Exec] : wrong with it -- " + str(e)   )
            
    def Exec_system(self, cmd):
        try:
            stdin, stdout, stderr = self.connect.exec_command(cmd)
            out = stdout.readlines()
            return out
        except Exception, e:
            self.ls.log_print("error", "[exec-system] : error is --- " + str(e))

    def Exec_noreturn(self,cmd):
        try:
            self.ls.log_print("system", "[exec-noreturn] " + str(cmd))
            stdin, stdout, stderr = self.connect.exec_command(cmd)
        except Exception,e:
            self.ls.log_print("system", "[SSH Exec-noreturn] : wrong with it -- " + str(e))
    
    def Close(self):
        try:
            self.connect.close()
        except Exception,e:
            self.ls.log_print("system", "[SSH Close] : wrong with it -- " + str(e))

class Sftp(object):
    def __init__(self,ipadd):
        self.ip = ipadd        
        self.ls = LogShow("SFTP")
        self.username = "root"
        self.password = "slamware123"

    def Connect(self):
        try:
            self.ls.log_print("system", "[Sftp connect] " + str(self.ip))
            self.sftp = paramiko.Transport(self.ip,22)
            self.sftp.connect(username=self.username,password=self.password)
            self.sf = paramiko.SFTPClient.from_transport(self.sftp)
        except Exception,e:
            self.ls.log_print("system", "[Sftp connect] : wrong with it -- " + str(e))

    def PutFile(self,localfile,remotefile):
        try:
            self.ls.log_print("system","[Sftp PutFile] : " + str(localfile) + " ====> " + str(remotefile))
            self.sf.put(localfile,remotefile)
            self.ls.log_print("system","[Sftp PutFile] : success")
        except Exception,e:
            self.ls.log_print("system","[Sftp PutFile] : wrong with it -- " + str(e))

    def GetFile(self,remotefile,localfile):
        try:
            self.ls.log_print("system","[Sftp GetFile] : " + str(localfile) + " <==== " + str(remotefile))
            self.sf.get(remotefile,localfile)
            self.ls.log_print("system","[Sftp GetFile] : success")
        except Exception,e:
            self.ls.log_print("system", "[Sftp GetFile] : wrong with -- " + str(e))
            
    def Close(self):
        self.sftp.close()


# sample to show how ssh use
if __name__ == "__main__":
    ssh = Ssh("192.168.11.1","root","slamware123")
    ssh.Connect()
    ssh.Exec("mv /etc/sdp_ref.json /home/root/sdp_ref.json ")
    ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref.json ")
    ssh.Exec("reboot -n")            
    ssh.Close()