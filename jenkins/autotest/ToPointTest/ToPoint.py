#encoding='utf-8'

'''
# version 0.1.1
# date 20170728
# author wei.meng @ slamtec
'''

import os,sys,json,time
from createreport import Report


class ToPoint(object):

    def __init__(self,ip):
        self.ip = ip

    def getJsonData(self):
         with open('topoint.conf') as json_file:
            self.data = json.load(json_file)
            self.resultall = []

    def getPointNum(self):
        self.pointnum =  self.data["pointnum"]

    def getTesttime(self):
        self.testtime = self.data["testtime"]

    def getDevia(self):
        self.devia = self.data["devia"]

    def getAllPoints(self):
        self.points = []
        self.points = self.data["points"] 

    def getResult(self):
        with open('result') as result:
            self.resultdata = json.load(result)[0]

    def runAuto(self):
        i = 1
        for point in self.points:
            os.system("Topointxy.exe " + self.ip + " " + str(point["x"]) + " " + str(point["y"]))
            self.getResult()
            self.resultall.append(self.resultdata)
            i = i + 1
        self.setWrite()
        
    def setWrite(self):
        f = open("testinfo.json","w")
        f.write(json.dumps(self.resultall))
        f.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print "[TP] wrong with argv"
        sys.exit(1)
    tp = ToPoint(ip)
    tp.getJsonData()
    tp.getPointNum()
    tp.getAllPoints()
    tp.runAuto()
    tp.setWrite()
    rep = Report("ToPoint Test")
    rep.runCreateTPReport(ip , "ZEUS TEST")
