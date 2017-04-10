'''
version : 1.0
author : wei.meng @ slamtec.inc


'''
import requests
import json
import sys,os
import time
import subprocess,traceback,platform

class Test_Move(object):
    def __init__(self):
        self.ip = 

    def Run(self,count,px,py):
        os.system("auto.exe " + self.ip + " " + str(count) + " " + str(px) + " " + str(py))

if __name__ == "__main__":
    
    flash = Flash()
    count = flash.getEnv("COUNT_OF_TEST")
    ip = flash.getEnv("DEVICE_IP")
    px = flash.getEnv("POINT_X")
    py = flash.getEnv("POINT_Y")
    move = Test_Move()
    move.Run(ip,count,px,py)