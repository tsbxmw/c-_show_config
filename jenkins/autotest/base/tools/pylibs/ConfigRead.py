# encoding='utf-8'
'''
#version : v1.1
#date : 20170425
#author : wei.meng@slamtec.com
#modify : 20170426 - add writetofile function to write the json info to a file named 'file.json' etc

'''
import os,sys
import json

class ConfigRead(object):
    def __init__(self):
        with open('config.config') as json_file:
            self.data = json.load(json_file)
    def getTestName(self):
        print self.data["TestInfo"]["TestName"]
        return self.data["TestInfo"]["TestName"]
    
    def getTest(self):
        print self.data["TestInfo"]["Test"]
        return self.data["TestInfo"]["Test"]

    def getTest_moveandcheck(self):
        print self.data["moveandcheck"]
        return self.data["moveandcheck"]

    def getTest_gohome(self):
        print self.data["gohome"]
        return self.data["gohome"]
    
    def WriteToFile(self,file,jsondata):
        jsonin = json.dumps(jsondata)
        f = open(file,'w')
        f.write(jsonin)
        f.close()

if __name__ == "__main__":
    cr = ConfigRead()
    cr.getTestName()
    cr.getTest()
    cr.getTest_moveandcheck()


    
