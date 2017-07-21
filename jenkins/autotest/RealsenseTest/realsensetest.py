# encoding='utf-8'

'''
# date    : 20170721
# author  : wei.meng@slamtec.com
# version : 1.0
'''

import os,sys,json,time
from debugmode import Root

class RealsenseTest(object):
    
    def __init__(self,ip):
        self.ip = ip
        self.result = {}
    def run(self):
        root = Root(self.ip)
        root.TestRealSense()
        
    def readresult(self):
        file = open("realsense.log","r")
        if "Success" in file.readline():
            print "[realsense] startup success"            
            self.result["result"] = "success"
        else:            
            self.result["result"] = "failed"
        file.close()
        
        self.WriteToFile("testinfo.json",self.result)
            
  
    def WriteToFile(self,filestr,jsondata):
        jsonin = json.dumps(jsondata)
        f = open(filestr,'w')
        f.write(jsonin)
        f.close()
        
if __name__ == "__main__":
    if len(sys.argv) > 1 :
        ip = sys.argv[1]
    else:
        print "[realsense] wrong with args"
        exit()
    rt = RealsenseTest(ip)
    rt.run()
    rt.readresult()
   