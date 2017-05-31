#-*- coding: utf-8 -*-
#!/usr/bin/python 

'''
# version : 1.3
# attention ：using paramiko module --- using 'pip install paramiko' to install the module
# functon : ssh and sftp function
# author : mengwei
# date : 2017.03.01
# modify : -add Sftp module to transport the file
# modify : 2017.03.02 - change the Ssh() to Ssh(ip,user,pass)
# modify : 2017.03.09 - change to the module
# modify : 2017.03.17 - add new function getfile
'''

import paramiko
import sys
import time

class Ssh(object):
    def __init__(self,ipadd,username,password):
        self.ip = ipadd
        self.username = username
        self.password = password

    def Connect(self):
        try:
            self.connect = paramiko.SSHClient()
            self.connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connect.connect(self.ip,22,self.username,self.password,timeout=5)
        except Exception,e:
            print "[SSH Connect] : wrong with it -- " + str(e)

    def Exec(self,cmd):
        try:
            print "[exec] " + str(cmd)
            stdin, stdout, stderr = self.connect.exec_command(cmd)
            out = stdout.readlines()
            return out
        except Exception,e:
            print "[SSH Exec] : wrong with it -- " + str(e)   
    def Exec_noreturn(self,cmd):
        try:
            print "[exec-noreturn] " + str(cmd)
            stdin, stdout, stderr = self.connect.exec_command(cmd)
        except Exception,e:
            print "[SSH Exec-noreturn] : wrong with it -- " + str(e)
    
    def Close(self):
        try:
            self.connect.close()
        except Exception,e:
            print "[SSH Close] : wrong with it -- " + str(e)

class Sftp(object):
    def __init__(self,ipadd):
        self.ip = ipadd
        self.username = "root"
        self.password = "slamware123"

    def Connect(self):
        try:
            self.sftp = paramiko.Transport(self.ip,22)
            self.sftp.connect(username=self.username,password=self.password)
            self.sf = paramiko.SFTPClient.from_transport(self.sftp)
        except Exception,e:
            print "[Sftp connect] : wrong with it -- " + str(e)

    def PutFile(self,localfile,remotefile):
        try:
           self.sf.put(localfile,remotefile)
        except Exception,e:
            print "[Sftp PutFile] : wrong with it -- " + str(e)

    def GetFile(self,remotefile,localfile):
        try:
            self.sf.get(remotefile,localfile)
        except Exception,e:
            print "[Sftp GetFile] : wrong with -- " + str(e)
            
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