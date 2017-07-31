#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
# version 0.0.1
# date 20170728
# author wei.meng @ slamtec
'''
import os,sys,json,time

class AutoRun(object):

    def __init__(self,ip):
        self.ip = ip

    def getJsonData(self):
         with open('autorun.conf') as json_file:
            self.data = json.load(json_file)

    def getPointNum(self):
        self.pointnum =  self.data["pointnum"]

    def getAllPoints(self):
        self.points = []
        self.points = self.data["points"] 
        
    def runAuto(self):
        for point in self.points:
            os.system("moveto.exe " + self.ip + " " + str(point["x"]) + " " + str(point["y"]))
        

if __name__ == "__main__":
    ar = AutoRun("10.16.130.129")
    ar.getJsonData()
    ar.getPointNum()
    ar.getAllPoints()
    ar.runAuto()
    