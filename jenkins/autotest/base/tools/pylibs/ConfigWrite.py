# encoding='utf-8'
'''
#version : v1.0
#date : 20170703
#author : wei.meng@slamtec.com
'''
import os,sys
import json
from SSH import Ssh,Sftp
import time

class ConfigWrite(object):
    def __init__(self):
        print("[ConfigWrite] = =")

    def WriteSlamwaredService(self,ip,user,password):
        print ("[ConfigWrite] write by ssh")
        ssh = Ssh(ip,user,password)
        ssh.Connect()
        ssh.Exec("systemctl stop slamwared")
        time.sleep(3)
        sftp = Sftp(ip)
        sftp.Connect()
        sftp.PutFile("..\\base\\tools\\config\\slamwared.service" , "/lib/systemd/system/slamwared.service")
        sftp.Close()
        time.sleep(3)
        ssh.Exec("if [ -f /home/root/slamware.stms ]; then rm /home/root/slamware.stms fi")
        time.sleep(3)
        ssh.Exec("systemctl daemon-reload")
        time.sleep(3)
        ssh.Exec("systemctl start slamwared")
        ssh.Close()


if __name__ == "__main__":
    cr = ConfigWrite()
    cr.WriteSlamwaredService("10.16.129.126","root","slamware123")
    
