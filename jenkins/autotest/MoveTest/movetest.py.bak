# encoding='utf-8'

'''
# date    : 20170426
# author  : wei.meng@slamtec.com
# version : 1.21
# modify  : 20170505 - add the info to the file
# modify  : 20170518 - complete the setup function
# modify  : 20170527 - bug fix1.20 - set map take 20s , we should sleep 30s to wait setting map complete.
'''
import os,sys,time,json
from ConfigRead import ConfigRead
from subprocess import Popen,PIPE
from createreport import Report

class MoveAndCheck(object):

    def __init__(self):
        self.cr = ConfigRead()
        self.jsondata = []
        
    # return the date-time 
    def timenow(self):
        return str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
    
    # show the MoveTest config info 
    def showTestInfo(self):
        data = self.cr.getTest()
        for d in data:
            print d
            if d["testname"] == "moveandcheck":
                pointnum = d["testpoint"]
                print "[MoveAndCheck] move and check test -- " + str(pointnum)

            if d["testname"] == "gohome":
                gohomenum = d["testtimes"]
                print "[MoveAndCheck] gohome test -- " + str(gohomenum) 

    # get the move and check points from configread
    def getMoveCheckPoints(self):
        self.points = []
        movecheck = self.cr.getTest_moveandcheck()
        for mc in movecheck["points"]:
            self.points.append([mc["pointx"],mc["pointy"],mc["a2num"],movecheck["checknum"],mc["result"]])
        print "[getMoveCheckPoints]" + str(self.points)
        return self.points
    
    # the test move and check
    def moveandcheck(self,ip,px,py,a2n,checknum,result):
        try:
            print "[moveandcheck] move to " + str(px) + "," + str(py) + " using a2-" + str(a2n) + " result-shouldbe-" + str(result) + " checknum" + str(checknum) + "%"
            os.system("moveandcheck.exe " + ip + " " + str(px) + " " + str(py) + " " + str(a2n) + " " + str(checknum))
            file = open("movetoxy.result",'r')
            resultf = file.readline()
            file.close()
            if (("success" in resultf ) and ( result == 1 ) ) or (("fail" in resultf) and (result == 0)) :
                print "[moveandcheck] move to " + str(px) + "," + str(py) + " using a2-" + str(a2n) + " test success"
                return True
            else :
                print "[moveandcheck] move to " + str(px) + "," + str(py) + " using a2-" + str(a2n) + " test fail"
                return False
        except:
            print "[moveandcheck] error"
    
    # get the gohome points from configread
    def getGoHomePoints(self):
        self.gohomeP = []
        gohome = self.cr.getTest_gohome()
        for gh in gohome["points"]:
            self.gohomeP.append([gh["pointx"],gh["pointy"],gohome["testtimes"]])
        print "[getGoHomePoints]" + str(self.gohomeP)
        return self.gohomeP

    # the test go home
    def gohome(self,ip,px,py,num):
        try:
            print "[gohome] move to  " + str(px) + "," + str(py) + " | " + str(num) 
            os.system("gohome.exe " + ip + " " + str(num)  + " " + str(px) + " " + str(py) )
            resultlist = []
            file = open("log\\gohome.log",'r')
            for f in file.readlines():
                tnum,result = f.split('-')
                resultlist.append({"timenow":self.timenow(),"ip":ip,"pointx":px,"pointy":py,"testnum":tnum,"result":result})
            file.close()
            return resultlist
        except:
            print "[gohome] error  -- "

    # run test all function
    def RunTest(self,ip,testname):
        try:
            if testname == "moveandcheck":               
                if os.path.exists(r'json\\moveandcheck.json'):
                    os.remove(r'json\\moveandcheck.json')
                mcjson = []
                for point in self.points:
                    result = self.moveandcheck(ip,point[0],point[1],point[2],point[3],point[4])
                    mcjson.append({"timenow":self.timenow(),"ip":ip,"pointx":point[0],"pointy":point[1],"a2num":point[2],"checknum":point[3],"result":result})
                self.WriteToFile("json\\moveandcheck.json",mcjson)
                
                self.jsondata.append({"moveandcheck":mcjson})
                return mcjson
            if testname == "gohome":
                if os.path.exists(r'log\\gohome.log'):
                    os.remove(r'log\\gohome.log')
                if os.path.exists(r'json\\gohome.json'):
                    os.remove(r'json\\gohome.json')
                ghjson = []
                for point in self.gohomeP:
                    result = self.gohome(ip,point[0],point[1],point[2])
                    ghjson = result
                self.WriteToFile("json\\gohome.json",ghjson)
                self.jsondata.append({"gohome":ghjson})
                return ghjson
            
            


        except:
            print "[RunTest] error -- "

    # write the test info json to the file
    def writetestinfo(self):
        self.WriteToFile("testinfo.json",self.jsondata)
        
    def WriteToFile(self,filestr,jsondata):
        jsonin = json.dumps(jsondata)
        f = open(filestr,'w')
        f.write(jsonin)
        f.close()

    def SetUp(self,ip):
        print "[setup] gohome now "
        print "[setup] set map now "
        os.system("..\\base\\tools\\win32tools\\zeustool.exe 24 " + ip +" map\\map.stcm")
        print "[MoveTest] set map over ."
        time.sleep(30)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print "[MoveAndCheck] error with sys.argv"
    ma = MoveAndCheck()
    ma.SetUp(ip)
    ma.showTestInfo()
    ma.getMoveCheckPoints()
    ma.getGoHomePoints()
    ma.RunTest(ip,"moveandcheck")
    ma.RunTest(ip,"gohome")
    ma.writetestinfo()
    report = Report("MoveTest")
    report.runCreateMoveTestReport(ip,"MoveTest")



    
