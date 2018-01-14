'''
# IpcControl.py
# get the video from the ipcamera
# author : wei.meng
# date : 20170820
'''

import os,time,sys

from datetime import datetime
from LogShow import LogShow
from slamwaredControl import SlamwaredControl
import threading
import time
import inspect
import ctypes
import subprocess

class getVideoLog(object):

    def __init__(self, ip, user, password, logpath):
        self.url = ip
        self.logpath = logpath
        self.user = user
        self.password = password
        objectname = "Get Video Log"
        self.ls = LogShow(objectname)
        self.ls.log_print("system", "start get log now ..")

    def _async_raise(self, tid, exctype):
        try:
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        except Exception,e:
            self.ls.log_print("debug", str(e))

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def getLogPath(self):
        self.localpath = os.path.split(os.path.realpath(__file__))[0]
        self.logexepath = os.path.abspath(os.path.join(self.localpath,"..\\win32tools\\log"))
        self.logexe =  self.logexepath + "\\getlog.exe"
        #self.ls.log_print("system", self.localpath)
        #self.ls.log_print("system", self.logexepath)
        self.ls.log_print("system", self.logexe)

    def getlog(self):
        self.ls.log_print("debug", "******")
        self.getLogPath()
        args = [self.url, self.user, self.password, self.logpath]
        self.popen = subprocess.Popen(self.logexe + " " + args[0] + " "  +  args[1] + " " +  args[2] + " " +  args[3])
        self.ls.log_print("debug", "******")


    def setthread(self):
        self.startlog = threading.Thread(target=self.getlog,args=())

    def stoplog(self):
        self.ls.log_print("system", "stop the video log now ")
        #self.stop_thread(self.startlog)
        #self.popen.kill()
        ctypes.windll.kernel32.TerminateProcess(int(self.popen._handle), -1)
        #os.killpg(self.popen.pid, signal.SIGTERM)
        self.ls.log_print("system", "stop video log success ")

    def startlog(self):
        #self.setthread()
        self.ls.log_print("system", "start the video log now ")
        #self.startlog.start()
        self.getlog()
        self.ls.log_print("system", "start video log success ")



