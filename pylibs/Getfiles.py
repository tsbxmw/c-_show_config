#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng
date : 2017.03.09
version : 1.01
modify : 20170606 - add function define "Getftpfile"
'''
import sys
import os
import time
from SSH import Ssh
from SSH import Sftp
from LogShow import LogShow

class Getfiles(object):
    def __init__(self):
        self.ls = LogShow("GetFile")
        self.ls.log_print ("system", "[getfiles]------------")
       
    def Getfile(self,remote,local):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote))
        self.ls.log_print ("system", "[getfile] local : " + str(local))
        copycmd = "xcopy /yse %s  %s\\ "%(remote,local)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")
            exit(1)
       
    def Getfile_filename(self,remote,local,filename):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote + "\\" + filename))
        self.ls.log_print ("system", "[getfile] local : " + str(local + "\\" + filename))
        copycmd = "echo F | xcopy /yse %s  %s "%(remote +"\\" + filename,local +"\\" + filename)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")
            exit(1)

    def Getfile_1(self,remote,local):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote))
        self.ls.log_print ("system", "[getfile] local : " + str(local))
        copycmd = "echo F | xcopy /yse %s  %s "%(remote,local)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")
            exit(1)
    

    
    def Getftpfile(self,remote,local):
        self.ls.log_print ("system", "[getftpfile] remote : " + str(remote))
        self.ls.log_print ("system", "[getftpfile] local  : " + str(local))

    def GetSCPfile(self,remote,local,ip):
        self.ls.log_print ("system", "[getscpfile] remote : " + str(remote))
        self.ls.log_print ("system", "[getscpfile] local  : " + str(local))
        sftp = Sftp(ip)
        sftp.Connect()
        sftp.GetFile(reomte,local)

    



