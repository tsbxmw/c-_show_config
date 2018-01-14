#! encoding='utf-8'

'''
# LogShow : LogShow()
# date : 20170811
# version : 0.2
# author : wei.meng
# m : 20170825 - key -> keys[key]
'''

import time
import os,sys

class LogShow(object):

    def __init__(self, logflag):
        self.logflag = logflag
        self.log_set_rank()

    def log_set_rank(self):
        self.log_rank = {
            "system" : "SYSTEM",
            "debug" : "DEBUG",
            "info" : "INFO", 
            "warn" : "WARN",
            "error" : "ERROR",
            "fatal" : "FATAL"
        }
        self.log_color = {
            "system" : "white",
            "debug" : "yellow",
            "info" : "blue", 
            "warn" : "red",
            "error" : "red",
            "fatal" : "red"
        }
        self.log_level_num = {
            "system" : 5 ,
            "debug"  : 4 ,
            "info"   : 3 ,
            "warn"   : 2 ,
            "error"  : 1 ,
            "fatal"  : 0 ,
        }

    def log_getsystime(self):
        return time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()) )

    def log_print(self, rank, log_str):
        log_string = self.log_getsystime() + " [ " + self.logflag + " ] (" + self.log_rank[rank] + ") " + str(log_str)
        print log_string

    def log_save_to_file(self, local, name):
        print "debug model"