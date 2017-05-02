#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
# author : wei.meng @ slamtec.inc
# date : 20170307
# version : 1.6
# modify : 20170311 - add css to html 
# modify : 20170313 - add create Flash One Build 
# modify : 20170323 - add create Daily Build
# modify : 20170327 - change to json
# modify : 20170407 -  add create Flash Dwon and Up build 
'''
import os, time, sys
import cgi,re
import shutil
import json

sys.path.append("pylib")
from SSH import Ssh
from debugmode import Root
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding( "utf-8")
class Report(object):

    def __init__(self):
        self.html1 = """<html>
        <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <title>"""
        self.html2 = """</title>
        <link rel="stylesheet" type="text/css" href="wcss.css" 
        </head>
        <body>"""
        

        
        self.css = """
        body {
            font:normal 80% verdana,arial,helvetica;
            color:#000000;
            background:#FDFFFF;
        }
        table tr td, table tr th {
            font-size: 68%;
        }
        .table-b table td{border:1px solid #F00} 
        table.details tr th{
            font-weight: bold;
            text-align:left;
            background:#E8FFC4;
        }
        table.details tr td{
            background:#D9FFFF;
        }

        table.general tr th{
            font-weight: bold;
            text-align:left;
            background:#4EFEB3;
        }
        table.general tr td{
            background:#FFFFDF;
        }


        p {
            line-height:1.5em;
            margin-top:0.5em; margin-bottom:1.0em;
        }
        h1 {
            margin: 0px 0px 5px; font: 250% verdana,arial,helvetica; text-align:center;
        }
        h2 {
            margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica; text-align:center;
        }
        h3 {
            margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica
        }
        h4 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h5 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h6 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        .error {
            font-weight:bold; color:red;
        }
        .fail {
            font-weight:bold; color:purple;
        }
        .pass {
            color:black;
        }
        .Properties {
          text-align:right;
        }
        """
        
        self.html2_new = """</title>
        <style type="text/css"> \n""" + self.css + """</style>\n</head>\n<body>"""
        
        self.html3 = """<h1>Test Report For """
        self.html4 = """</h1>"""
        self.html5 = """<div style="text-indent:3em">
        <br/><br/>
        </div>
        </body>
        </html>"""
        self.addcsstohtmlstart = """<style type="text/css">"""
        self.addcsstohtmlend = """</style>"""
        self.report_name = """summary.html"""
        self.title_name = ""
        self.tStatistics = None
        self.deviceinfo = {}
        self.flashonebuild = False
        self.flashdailybuild = False
        self.flashdownandupbuild = False
        self.movetest = False


    def createReport(self,test_name):
        self.title_name = test_name
        self.tStatistics = open("..\\testdata\\report\\"+ self.report_name , 'wb')
        self.tStatistics.write( self.html1)
        self.tStatistics.write( self.title_name + " TEST REPORT")
        self.tStatistics.write( self.html2_new)
        self.tStatistics.write( self.html3)
        self.tStatistics.write( self.title_name)
        self.tStatistics.write( self.html4)

    def getDeviceInfo(self,ipadd):
        root = Root(ipadd)
        i = 1
        while True: 
            print ("try " + "times " + str(i))
            try:
                root.Login().raise_for_status()
            except:
                print "[login] waitting for login successfully"
                time.sleep(10)
                i = i + 1
                continue
            try:
                self.deviceinfo["Device S/N"] = root.GetSN() 
                self.deviceinfo["S/N"] = root.GetSN_1()
                self.deviceinfo["Ip address"] = root.GetIpMode()
            except:
                print "[GetSN] GetSN wrong"
                time.sleep(10)
                i = i + 1
                continue
            try:
                self.deviceinfo["FirmWare version"] = root.Getversion()
            except:
                print "[getversion] getversion wrong"
                time.sleep(10)
                i = i + 1
                continue
                    
            break

    def getadd_Flash_Daily_Build_Info(self):
        output = open("..\\testdata\\report\\json\\Flash Daily Build.json","r")
        self.jsoninfo_flashdailybuild = json.load(output)
        output.close()
        self.flashdailybuild = True
    
    def getadd_Flash_One_Build_Info(self):
        output = open("..\\testdata\\report\\json\\Flash One Build.json","r")
        testinfo = json.load(output)
        output.close()
        self.jsoninfo_flashonebuild = {}
        for info in testinfo:
            if info["time"] == "0":
                self.jsoninfo_flashonebuild["count"] = info["count"]
            if info["time"] == "1":
                self.jsoninfo_flashonebuild["begin"] = (info["values"])["begin"]
                self.jsoninfo_flashonebuild["version_before"] = (info["values"])["version_before"]
                self.jsoninfo_flashonebuild["version_file"] = (info["values"])["version_file"]
            if info["time"] == self.jsoninfo_flashonebuild["count"]:
                self.jsoninfo_flashonebuild["end"] = (info["values"])["end"]
        self.flashonebuild = True

    def getadd_Flash_Down_and_Up_Info(self):
        output = open("..\\testdata\\report\\json\\Flash Down and Up.json","r")
        testinfo = json.load(output)
        output.close()
        self.jsoninfo_flashdownandupbuild = {}
        for info in testinfo:
            if info["time"] == "0":
                self.jsoninfo_flashdownandupbuild["count"] = info["count"]
            if info["time"] == "1":
                self.jsoninfo_flashdownandupbuild["begin"] = info["down_values"]["down_begin"]
                self.jsoninfo_flashdownandupbuild["version_before"] = info["down_values"]["version_down_before"]
                self.jsoninfo_flashdownandupbuild["version_down_file"] = info["down_values"]["version_down_file"]
                self.jsoninfo_flashdownandupbuild["version_up_file"] = info["up_values"]["version_up_file"]
            if info["time"] == self.jsoninfo_flashdownandupbuild["count"]:
                self.jsoninfo_flashdownandupbuild["version_after"] = info["up_values"]["version_up_after"]
                self.jsoninfo_flashdownandupbuild["end"] = info["up_values"]["up_end"]
        self.flashdownandupbuild = True
        
    def byteify(self,input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
            
    def getadd_MoveTest_Info(self):
        self.jsoninfo_gohome = {}
        self.jsoninfo_movetest = {}
        output = open("..\\testdata\\report\\json\\MoveTest.json",'r')
        macjsondata = json.loads(output.readline().decode('utf-8'),encoding='utf-8')
        output.close()
        majd = self.byteify(macjsondata)
        mci = 0
        i = 0
        j = 0
        ghi = 0
        for mcjdx in majd:
            
            
            if "moveandcheck" in mcjdx:
                for mcjd in mcjdx["moveandcheck"]:
                    if i == 0:
                        self.jsoninfo_movetest["time"] = mcjd["timenow"]
                        
                    if mcjd["result"]:
                        mci = mci + 1
                    i = i + 1
            if "gohome" in mcjdx:
                for mcjd in mcjdx["gohome"]:
                    if j == 0:
                        self.jsoninfo_gohome["time"] = mcjd["timenow"]
                        
                    if "success" in mcjd["result"]:
                        ghi = ghi + 1
                    j = j + 1
                    
        self.jsoninfo_movetest["success"] = mci
        self.jsoninfo_movetest["all"] = i
        self.jsoninfo_gohome["success"] = ghi
        self.jsoninfo_gohome["all"] = j
        print self.jsoninfo_movetest
        print self.jsoninfo_gohome
        self.movetest = True
        
        
    def addDeviceInfo(self):
        self.tStatistics.write("<div><br/></div><h2>Device Info</h2>\n")
        self.tStatistics.write("<table class=\"general\" border=\"0\" cellpadding=\"5\" cellspacing=\"2\" width=\"95%\">\n")
        self.tStatistics.write("<tr><th width=\"20%\">Name</th><th width=\"30%\">Value</th><th width=\"20%\">Name</th><th width=\"30%\">Value</th></tr>\n")
        self.tStatistics.write("<tr><td>FirmWare version </td> <td>" + str(self.deviceinfo["FirmWare version"]) + "</td><td>Device S/N </td> <td>" + str(self.deviceinfo["Device S/N"]) + "</td></tr>\n")
        self.tStatistics.write("<tr><td>S/N </td> <td>" + str(self.deviceinfo["S/N"]) + "</td><td>Ip address </td> <td>" + str(self.deviceinfo["Ip address"]) + "</td><tr>")
        #self.tStatistics.write("<tr><td>Ip address </td> <td>" + deviceinfo["Ip address"] + "</td><td>Device S/N </td> <td>" + deviceinfo["Device S/N"] + "</td><tr>")
        self.tStatistics.write("</table>")

    def addInfo(self):
        self.report_dir="\\\\10.254.1.27\\TestReport\\" + os.getenv("JOB_NAME") + "\\" + os.getenv("BUILD_NUMBER") + "\\"
        
        self.tStatistics.write("<div><br/></div><h2>Flash Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\"  cellpadding=\"5\" cellspacing=\"2\" width=\"95%\">\n")
        self.tStatistics.write("<tr><th width=\"10%\">buildname</th><th>Begin Time</th><th>End Time</th><th>others</th><th>Link</th></tr>\n")
        if self.flashdailybuild :
            self.tStatistics.write("<tr><td>Flash Daily Build</td><td>"+self.jsoninfo_flashdailybuild["begin"]+"</td><td>" + self.jsoninfo_flashdailybuild["end"] 
                 + "</td><td> version before : " + self.jsoninfo_flashdailybuild["version_before"] + " | version file : " + self.jsoninfo_flashdailybuild["version_file"] 
                + "</td><td><a href=\"" + self.report_dir + "Flash Daily Build.html\">"+"link"+"</a></td></tr>\n")
        if self.flashonebuild :
            self.tStatistics.write("<tr><td>Flash One Build</td><td>"+self.jsoninfo_flashonebuild["begin"]+"</td><td>" + self.jsoninfo_flashonebuild["end"] 
                 + "</td><td> version before : " + self.jsoninfo_flashonebuild["version_before"] + " | version file : " + self.jsoninfo_flashonebuild["version_file"] + " | test count :" 
                 + self.jsoninfo_flashonebuild["count"]+ "</td><td><a href=\"" + self.report_dir + "Flash One Build.html\">"+"link"+"</a></td></tr>\n")
        if self.flashdownandupbuild :
            self.tStatistics.write("<tr><td>Flash Down and Up</td><td>"+self.jsoninfo_flashdownandupbuild["begin"]+"</td><td>" + self.jsoninfo_flashdownandupbuild["end"] 
                 + "</td><td> version before : " + self.jsoninfo_flashdownandupbuild["version_before"] + " | version up file : " 
                 + self.jsoninfo_flashdownandupbuild["version_up_file"] + " | version down file : " 
                 + self.jsoninfo_flashdownandupbuild["version_down_file"] + " | test count :" 
                 + self.jsoninfo_flashdownandupbuild["count"]+ "</td><td><a href=\"" + self.report_dir + "Flash Down and Up.html\">"+"link"+"</a></td></tr>\n")
            
        self.tStatistics.write("</table>\n")
    
    def addMoveInfo(self):
        self.report_dir="\\\\10.254.1.27\\TestReport\\" + os.getenv("JOB_NAME") + "\\" + os.getenv("BUILD_NUMBER") + "\\"
        
        self.tStatistics.write("<div><br/></div><h2>Move Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\"  cellpadding=\"5\" cellspacing=\"2\" width=\"95%\">\n")
        self.tStatistics.write("<tr><th width=\"10%\">build-name</th><th>test date</th><th>test-times</th><th>success-times</th><th>others</th><th>Link</th></tr>\n")
        if self.movetest:
            self.tStatistics.write("<tr><td>movetest</td><td>" + str(self.jsoninfo_movetest["time"]) + "</td><td>" + str(self.jsoninfo_movetest["all"]) + "</td><td>" + str(self.jsoninfo_movetest["success"]) + "</td><td>nothing</td><td><a href=\"" + self.report_dir + "MoveTest.html\">link</a></td></tr>\n")
            self.tStatistics.write("<tr><td>gohome</td><td>" + str(self.jsoninfo_gohome["time"]) + "</td><td>" + str(self.jsoninfo_gohome["all"]) + "</td><td>" + str(self.jsoninfo_gohome["success"]) + "</td><td>nothing</td><td><a href=\"" + self.report_dir + "MoveTest.html\">link</a></td></tr>\n")
        self.tStatistics.write("</table>\n")

    def endReport(self):
        self.tStatistics.write( self.html5)
        self.tStatistics.close()

    def createCSS(self):
        self.tCss = open("..\\testdata\\report\\wcss.css" , 'wb')
        self.tCss.write(self.css)
        self.tCss.close()

if __name__ == "__main__":
    #deviceinfo = {"FirmWare version":"zeus_edison.2.2.1_rtm.20170308.bin","Device S/N":"D58F4024E0EDF790D4E9F2F9075483E4","Ip address":"192.168.11.1","S/N":" C47ADDC6F19575BD90A14AC5"}
    
    if len(sys.argv) > 2 :
        ip = sys.argv[1]
        productname = sys.argv[2]
    else :
        print "[create report] wrong with sys.argv"
        sys.exit(1)
    teststage = os.getenv("TEST_STAGES")
    
    report = Report()
    report.createCSS()
    report.createReport(productname)
    
    report.getDeviceInfo(ip)
    report.addDeviceInfo()
    if "Flash Daily Build" in teststage:
        report.getadd_Flash_Daily_Build_Info()
    if "Flash One Build" in teststage:
        report.getadd_Flash_One_Build_Info()
    if "Flash Down and Up" in teststage:
        report.getadd_Flash_Down_and_Up_Info()
    if "MoveTest" in teststage:
        report.getadd_MoveTest_Info()
    report.addMoveInfo()
    report.addInfo()
    report.endReport()