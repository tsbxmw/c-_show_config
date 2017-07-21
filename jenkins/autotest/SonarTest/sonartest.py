# encoding='utf-8'

'''
# date    : 20170721
# author  : wei.meng@slamtec.com
# version : 1.0
'''
import os,sys,time,json

class SonarTest(object):
    def __init__(self,deviceip):
        self.deviceip = deviceip
        self.rootdir = os.getcwd()
        self.result = {}
        self.id = ["6", "7", "8", "9", "10"]
        self.point = {}
        self.point["x"] = "0.11"
        self.point["y"] = "4.95"
        
    def readresult(self):
        file = open("result","r")
        for f in file.readlines():
            if f != "" and f  != "\n" :
                f = f.replace("\n","")
                sonarid,sonarresult = f.split("--")
                self.result[sonarid] = sonarresult
                print sonarid + "--" + sonarresult
        file.close()
        
        for id in self.id:
            print self.result[id]
        
        self.WriteToFile("testinfo.json",self.result)
            
  
    def WriteToFile(self,filestr,jsondata):
        jsonin = json.dumps(jsondata)
        f = open(filestr,'w')
        f.write(jsonin)
        f.close()
        
    def run(self):
        try:
            os.chdir(self.rootdir)
            cmdstr = "TestCase_sonartest.exe " + self.deviceip + " " + str(self.point["x"]) + " " + str(self.point["y"])
            os.system(cmdstr)
        except Exception,e:
            print "[sonar] test wrong with " + str(e)

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print "[MoveAndCheck] error with sys.argv"
    sonar = SonarTest(ip)
    sonar.run()
    sonar.readresult()