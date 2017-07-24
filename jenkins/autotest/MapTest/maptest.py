'''
# Map test 
# version 1.0
# date 2017.7.24
# test map upload and download from zeus
'''

import sys,os,time,json

class MapTest(object):
    def __init__(self,ip,loadpath,savepath):
        self.ip = ip
        self.loadpath = loadpath
        self.savepath = savepath
        self.logtest = "[maptest] "
        self.result = {}

    def MapUpload(self):
        try:
            print self.logtest + " start upload map.stcm to zeus"
            os.system("map.exe " + self.ip + " 1 " + self.loadpath)            
            time.sleep(30)
            self.result["upload"] = "success"
        except Exception,e:
            self.result["upload"] = "failed"
            print self.logtest + str(e)

    def MapDownload(self):
        try:
            print self.logtest + " start download map to local"
            os.system("map.exe " + self.ip + " 2 " + self.savepath)
            time.sleep(30)
            self.result["download"] = "success"
        except Exception,e:
            self.result["download"] = "failed"
            print self.logtest + str(e)

    def SetUp(self):
        try:
            if os.path.exists(self.loadpath):
                print self.logtest + "<load path>" + self.loadpath + " check ok"
            else :
                print self.logtest + "do not find the map "
                sys.exit(1)
            if os.path.exists(self.savepath):
                print self.logtest + "<save path> delete the save path now "
                os.remove(self.savepath)
            else :
                print self.logtest + "<save path>" + self.savepath + " check ok"
        except Exception,e:
            print self.logtest + str(e)

    def run(self):
        self.WriteToFile("testinfo.json",self.result)

    def WriteToFile(self,filestr,jsondata):
        jsonin = json.dumps(jsondata)
        f = open(filestr,'w')
        f.write(jsonin)
        f.close()




if __name__ == "__main__":
    if len(sys.argv) > 3 :
        ip = sys.argv[1]
        loadPath = sys.argv[2]
        savePath = sys.argv[3]
    else:
        print "wrong with args"
        sys.exit(1)
    mt = MapTest(ip, loadPath, savePath)
    mt.SetUp()
    mt.MapUpload()
    mt.MapDownload()
    mt.run()
