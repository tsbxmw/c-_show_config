#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng @ slamtec.inc
date : 2017.03.09
version : 1.01
modify : 20170606 - add function define "Getftpfile"
'''
import sys
import os
import time

class Getfiles(object):
    def __init__(self):
        print ("[getfiles]------------")
       
    def Getfile(self,remote,local):
        print ("[getfile] remote: " + str(remote))
        print ("[getfile] local : " + str(local))
        copycmd = "xcopy /yse %s  %s\\ "%(remote,local)
        print ("[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            print ("[getfile] copy ok")
        else:
            print ("[getfile] copy fail")
            exit(1)
    
    def Getftpfile(self,remote,local):
        print ("[getftpfile] remote : " + str(remote))
        print ("[getftpfile] local  : " + str(local))
