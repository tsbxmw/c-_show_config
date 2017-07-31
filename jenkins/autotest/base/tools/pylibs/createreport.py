#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : mengwei @ slamtec.com inc
date : 20170313
version : 2.0
create report for all stage report - with new fuction to create stage report and statis report
modify : 20170427 - add moveandcheck test report creator function
'''
import os, time, sys
import cgi,re
import json
import shutil

#sys.path.append("pylib")
from SSH import Ssh
from debugmode import Root
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding( "utf-8")

class Report(object):

    def __init__(self,testname):
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

        self.html3 = """<h1>Test Report For """
        self.html4 = """</h1>"""
        self.html5 = """<div style="text-indent:3em">
        <br/><br/>
        </div>
        </body>
        </html>"""
        self.report_name = """report.html"""
        self.title_name = ""
        self.tStatistics = None
        self.deviceinfo = {}
        self.testname = testname


    def createReport(self,test_name):
        self.title_name = test_name
        self.tStatistics = open(".\\report\\"+ self.report_name , 'wb')
        self.tStatistics.write( self.html1)
        self.tStatistics.write( self.title_name + " TEST REPORT")
        self.tStatistics.write( self.html2)
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



    def addDeviceInfo(self):
        self.tStatistics.write("<div><br/></div><h2>Device Info</h2>\n")
        self.tStatistics.write("<table class=\"general\" align=\"center\" border=\"0\" cellpadding=\"5\" cellspacing=\"3\" width=\"70%\">\n")
        self.tStatistics.write("<tr><th width=\"15%\">Name</th><th width=\"20%\">Value</th><th width=\"15%\">Name</th><th width=\"20%\">Value</th></tr>\n")
        self.tStatistics.write("<tr><td>FirmWare version </td> <td>" + str(self.deviceinfo["FirmWare version"]) + "</td><td>Device S/N </td> <td>" + str(self.deviceinfo["Device S/N"]) + "</td></tr>\n")
        self.tStatistics.write("<tr><td>S/N </td> <td>" + str(self.deviceinfo["S/N"]) + "</td><td>Ip address </td> <td>" + str(self.deviceinfo["Ip address"]) + "</td><tr>")
        #self.tStatistics.write("<tr><td>Ip address </td> <td>" + deviceinfo["Ip address"] + "</td><td>Device S/N </td> <td>" + deviceinfo["Device S/N"] + "</td><tr>")
        self.tStatistics.write("</table>")

    def addInfo(self):
        self.tStatistics.write("<div><br/></div><h2>Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\"  cellpadding=\"5\" cellspacing=\"2\" width=\"95%\">\n")
        self.tStatistics.write("<tr><th width=\"30%\">buildname</th><th>Passed</th><th>Failed</th><th>Begin Time</th><th>End Time</th><th>Link</th></tr>\n")
        self.tStatistics.write("<tr><td>Daily Update</td><td>"+"xxx"+"</td><td>"+"xxxx"+"</td><td>"+"xxxx"+"</td><td>"+"xxxx"+"</td><td><a href=??>"+"xxxx"+"</a></td></tr>\n")
        self.tStatistics.write("<tr><td>Map Build</td><td>"+"xxx"+"</td><td>"+"xxx"+"</td><td>"+"xxxx"+"</td><td>"+"xxxx"+"</td><td><a href=??>"+"xxxx"+"</a></td></tr>\n")
        self.tStatistics.write("</table>\n")

   
   
   
    def getStageInfo(self):
        output = open("testinfo.json","r")
        '''
        for line in output.readlines():
            str1,str2 = line.split("=")
            if str1 == "version_before" :
                self.version_before = str2
            if str1 == "begin":
                self.begintime = str2
            if str1 == "end" :
                self.endtime = str2
            if str1 == "version_file":
                self.version_file = str2
            if str1 == "timeuse":
                self.timeuse = str2'''
        
        self.jsoninfo = json.load(output)
        output.close()
        self.version_after = self.deviceinfo["FirmWare version"]
        
    def getaddStageOneBuildInfo(self):
        output = open("testinfo.json","r")
        testinfo = json.load(output)
        output.close()
        self.info_onbuild = {}
        self.version_after = self.deviceinfo["FirmWare version"]
        for info in testinfo:
            if info["time"] == "0":
                self.info_onbuild["count"] = info["count"]
            if info["time"] == "1":
                self.info_onbuild["start"] = (info["values"])["begin"]
                self.info_onbuild["version_before"] = (info["values"])["version_before"]
                self.info_onbuild["version_file"] = (info["values"])["version_file"]
            if info["time"] == self.info_onbuild["count"]:
                self.info_onbuild["end"] = (info["values"])["end"]
             
        for info in testinfo:
            if info["time"] == "0":
                self.tStatistics.write("<div><br/></div><h2> " + self.testname + " Test Statistics</h2>\n")
                self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
                self.tStatistics.write("<tr><th width=\"30%\">version_before</th><th>version_after</th><th>version_file</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ self.info_onbuild["version_before"] +"</td><td>"+ self.version_after +"</td><td>" + self.info_onbuild["version_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">All Count</th><th>Begin Time</th><th>End Time</th></tr>\n")
                self.tStatistics.write("<tr><td>" + self.info_onbuild["count"] + "</td><td>"+ self.info_onbuild["start"] +"</td><td>" + self.info_onbuild["end"] + "</td></tr>\n")
                self.tStatistics.write("</table>\n")
            else:
                self.tStatistics.write("<div><br/></div><h2> " + self.testname + " -- " + info["time"] + " Test Statistics</h2>\n")
                self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
                self.tStatistics.write("<tr><th width=\"30%\">version_before</th><th>version_after</th><th>version_file</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ (info["values"])["version_before"] +"</td><td>"+ (info["values"])["version_after"] +"</td><td>" + (info["values"])["version_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">Begin Time</th><th>End Time</th><th>Time Use (s)</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ (info["values"])["begin"] +"</td><td>" + (info["values"])["end"] + "</td><td> " + (info["values"])["timeuse"] +"</td></tr>\n")
                self.tStatistics.write("</table>\n")
            
            
    def getaddStageDownUpBuildInfo(self):
        output = open("testinfo.json","r")
        testinfo = json.load(output)
        output.close()
        self.version_after = self.deviceinfo["FirmWare version"]
        self.info_downup = {}
        for info in testinfo:
            if info["time"] == "0":
                self.info_downup["count"] = info["count"]
            if info["time"] == "1":
                self.info_downup["up_begin"] = (info["up_values"])["up_begin"]
                self.info_downup["version_up_before"] = (info["up_values"])["version_up_before"]
                self.info_downup["version_up_file"] = (info["up_values"])["version_up_file"]
                self.info_downup["down_begin"] = (info["down_values"])["down_begin"]
                self.info_downup["version_down_before"] = (info["down_values"])["version_down_before"]
                self.info_downup["version_down_file"] = (info["down_values"])["version_down_file"]
                
            if info["time"] == self.info_downup["count"]:
                self.info_downup["up_end"] = (info["up_values"])["up_end"]
                self.info_downup["down_end"] = (info["down_values"])["down_end"]
             
        for info in testinfo:
            if info["time"] == "0":
                self.tStatistics.write("<div><br/></div><h2> " + self.testname + " Test Statistics</h2>\n")
                self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
                self.tStatistics.write("<tr><th width=\"30%\">down_version_before</th><th>version_now</th><th>down_version_file</th></tr>\n")
                self.tStatistics.write("<tr><td>" + self.info_downup["version_down_before"] +"</td><td>"+ self.version_after +"</td><td>" + self.info_downup["version_down_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">up_version_before</th><th>version_now</th><th>up_version_file</th></tr>\n")
                self.tStatistics.write("<tr><td>" + self.info_downup["version_up_before"] +"</td><td>"+ self.version_after +"</td><td>" + self.info_downup["version_up_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">All Count</th><th>Begin Time</th><th>End Time</th></tr>\n")
                self.tStatistics.write("<tr><td>" + self.info_downup["count"] + "</td><td>"+ self.info_downup["down_begin"] +"</td><td>" + self.info_downup["up_end"] + "</td></tr>\n")
                self.tStatistics.write("</table>\n")
            else:
                self.tStatistics.write("<div><br/></div><h2> " + self.testname + " -- " + info["time"] + " Test Statistics</h2>\n")
                self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
                self.tStatistics.write("<tr><th width=\"30%\">version_down_before</th><th>version_after</th><th>version_file</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ (info["down_values"])["version_down_before"] +"</td><td>"+ (info["down_values"])["version_down_after"] +"</td><td>" + (info["down_values"])["version_down_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">Down Begin Time</th><th>Down End Time</th><th>Down Time Use (s)</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ (info["down_values"])["down_begin"] +"</td><td>" + (info["down_values"])["down_end"] + "</td><td> " + (info["down_values"])["down_timeuse"] +"</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">version_up_before</th><th>version_up_after</th><th>version_up_file</th></tr>\n")                                
                self.tStatistics.write("<tr><td>"+ (info["up_values"])["version_up_before"] +"</td><td>"+ (info["up_values"])["version_up_after"] +"</td><td>" + (info["up_values"])["version_up_file"] + "</td></tr>\n")
                self.tStatistics.write("<tr><th width=\"30%\">Up Begin Time</th><th>Up End Time</th><th>Up Time Use (s)</th></tr>\n")
                self.tStatistics.write("<tr><td>"+ (info["up_values"])["up_begin"] +"</td><td>" + (info["up_values"])["up_end"] + "</td><td> " + (info["up_values"])["up_timeuse"] +"</td></tr>\n")
                self.tStatistics.write("</table>\n")
    
    def byteify(self,input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
            
    def getaddStageMoveTestInfo(self):
        output = open("json\\moveandcheck.json",'r')
        macjsondata = json.loads(output.readline().decode('utf-8'),encoding='utf-8')
        output.close()
        majd = self.byteify(macjsondata)
        print majd
        self.tStatistics.write("<div><br/></div><h2> move and check Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
        self.tStatistics.write("<tr><th>num</th><th width=\"30%\">test-time</th><th>point-x</th><th>point-y</th><th>a2 num</th><th>result</th></tr>\n")
        i = 1
        for jd in majd :
            print jd
            if jd["result"] :
                self.tStatistics.write("<tr><td>"+ str(i) + "</td><td>" + str(jd["timenow"]) +"</td><td>"+ str(jd["pointx"]) +"</td><td>" + str(jd["pointy"]) + "</td><td>" + str(jd["a2num"]) + "</td><td bgcolor=\"#00EC00\">" + str(jd["result"]) + "</td></tr>\n")
            else:
                self.tStatistics.write("<tr><td>"+ str(i) + "</td><td>" + str(jd["timenow"]) +"</td><td>"+ str(jd["pointx"]) +"</td><td>" + str(jd["pointy"]) + "</td><td>" + str(jd["a2num"]) + "</td><td bgcolor=\"#EA0000\">" + str(jd["result"]) + "</td></tr>\n")
                
            i = i + 1
        self.tStatistics.write("</table>\n")
        
        output = open("json\\gohome.json",'r')
        ghjsondata = json.load(output)
        output.close()
        ghjd = self.byteify(ghjsondata)
        print majd
        
        self.tStatistics.write("<div><br/></div><h2> Go Home Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
        self.tStatistics.write("<tr><th>num</th><th width=\"30%\">test-time</th><th>point-x</th><th>point-y</th><th>testnum</th><th>result</th></tr>\n")
            
        i = 1
        for jd in ghjd :
            if "success" in jd["result"] :
                self.tStatistics.write("<tr><td>"+ str(i) + "</td><td>" + str(jd["timenow"]) +"</td><td>"+ str(jd["pointx"]) +"</td><td>" + str(jd["pointy"]) + "</td><td>" + str(jd["testnum"]) + "</td><td bgcolor=\"green\">" + str(jd["result"]) + "</td></tr>\n")
            else:
                self.tStatistics.write("<tr><td>"+ str(i) + "</td><td>" + str(jd["timenow"]) +"</td><td>"+ str(jd["pointx"]) +"</td><td>" + str(jd["pointy"]) + "</td><td>" + str(jd["testnum"]) + "</td><td bgcolor=\"red\">" + str(jd["result"]) + "</td></tr>\n")
            i = i + 1
        self.tStatistics.write("</table>\n")
        

    def addStageInfo(self):
        self.tStatistics.write("<div><br/></div><h2> " + self.testname + " Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
        self.tStatistics.write("<tr><th width=\"30%\">version_before</th><th>version_after</th><th>version_file</th></tr>\n")
        self.tStatistics.write("<tr><td>"+ self.jsoninfo["version_before"] +"</td><td>"+ self.version_after +"</td><td>" + self.jsoninfo["version_file"] + "</td></tr>\n")
        self.tStatistics.write("<tr><th width=\"30%\">Begin Time</th><th>End Time</th><th>Time Use (s)</th></tr>\n")
        self.tStatistics.write("<tr><td>"+ self.jsoninfo["begin"] +"</td><td>" + self.jsoninfo["end"] + "</td><td> " + self.jsoninfo["timeuse"] +"</td></tr>\n")
        self.tStatistics.write("</table>\n")

    def addToPointInfo(self):
        output = open("testinfo.json",'r')
        tpjsondata = json.load(output)
        output.close()
        tpjd = self.byteify(tpjsondata)
        print tpjd
        self.tStatistics.write("<div><br/></div><h2> To Point Test Statistics</h2>\n")
        self.tStatistics.write("<table class=\"general\" align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
        self.tStatistics.write("<tr><th>num</th>><th>point-x</th><th>point-y</th><th>real-x</th><th>real-y</th><th>result</th></tr>\n")
        i = 1
        for jd in tpjd :
            print jd
            print type(jd) == type({})
            self.tStatistics.write("<tr><td>"+ str(i) + "</td><td>"+ jd["x"] +"</td><td>" + jd["y"] + "</td><td>"+ jd["x1"] +"</td><td>" + jd["y1"] + "</td><td>" + jd["divresult"] + "</td></tr>\n")
            i = i + 1
        self.tStatistics.write("</table>\n")

    def endReport(self):
        self.tStatistics.write( self.html5)
        self.tStatistics.close()

    def createCSS(self):
        self.tCss = open(".\\report\\wcss.css" , 'wb')
        self.tCss.write(self.css)
        self.tCss.close()

    def runCreateTPReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        self.addToPointInfo()
        self.endReport()

    def runCreateReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        self.getStageInfo()
        self.addStageInfo()
        self.endReport()
        
        
    def runCreateWrongReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        self.getStageInfo()
        self.addStageInfo()
        self.endReport()
    
    def runCreateOneBuildReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        #report.addInfo()
        self.getaddStageOneBuildInfo()
        self.endReport()
    
    def runCreateDownUpBuildReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        #report.addInfo()
        self.getaddStageDownUpBuildInfo()
        self.endReport()    
    
    def runCreateMoveTestReport(self,ip,productname):
        self.createCSS()
        self.createReport(productname)
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        #report.addInfo()
        self.getaddStageMoveTestInfo()
        self.endReport()   
    
   
        
if __name__ == "__main__":
    #deviceinfo = {"FirmWare version":"zeus_edison.2.2.1_rtm.20170308.bin","Device S/N":"D58F4024E0EDF790D4E9F2F9075483E4","Ip address":"192.168.11.1","S/N":" C47ADDC6F19575BD90A14AC5"}
    
    if len(sys.argv) > 3 :
        ip = sys.argv[1]
        productname = sys.argv[2]
        testname = sys.argv[3]
    else :
        print "[create report] wrong with sys.argv"
        sys.exit(1)
      
    report = Report()
    report.createCSS()
    report.createReport(productname)
    report.getDeviceInfo(ip)
    report.addDeviceInfo()
    #report.addInfo()
    report.getStageInfo()
    report.addStageInfo()
    report.endReport()