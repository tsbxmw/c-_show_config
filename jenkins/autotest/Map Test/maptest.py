'''
# Map test 
# version 1.0
# date 2017.7.24
# test map upload and download from zeus
'''

import sys,os,time

class MapTest(object):
    def __init__(self,ip,loadpath,savepath):
        self.ip = ip
        self.loadpath = loadpath
        self.savepath = savepath

    def MapUpload(self):
        try:
            os.system("map.exe " + ip + " 1 " + loadpath)
        except Exception,e:
            print str(e)
