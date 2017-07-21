'''
# version 1.0
# date 20170719
# author wei.meng@slamtec.com

'''
import os
class createFailReport(object):
    def __init__(self):
        self.tStatistics = open(".\\report.html" , 'wb')
        
    def getchangelog(self):
        infos=[]
        f = open(".\\gitchangelog.txt","r")
        modules = ["agent","sdp","sdk","firmwares/base","firmwares/cp0","firmwares/ui","firmwares/zeus","platforms/edison","platforms/phoenix"]
        loginfo = {}
        i = 0
        for line in f.readlines():
            if line.replace("\n","") in modules:
                print line
                project = line
                continue
            if i == 1:

                if (not line.startswith("commit")) and (not line.startswith("Author")) and (not line.startswith("Date")) and (not line.startswith(":"))  :
                    loginfo["info"] = loginfo["info"] + line
                else :
                    if ( line.startswith(":") or line.startswith("commit") ):
                        print loginfo["project"]
                        infos.append(loginfo)
                        i = 0
                    else :                        
                        if (not line.startswith("Date") ) and (not line.startswith("Author")) :
                            infos.append(loginfo)
                            i = 0
            if i == 1 and line.startswith("Date"):
                date,space,space,loginfo["week"],loginfo["month"],loginfo["day"],loginfo["time"],loginfo["year"],nouse = line.split(" ")
            if i == 1 and line.startswith("Author"):
                author = []
                author = line.split(" ")
                loginfo["name"] = " "
                for a in author:
                    if a.startswith("<"):
                        loginfo["email"] = a
                    if a == "Author:":
                        print " "
                    else:
                        loginfo["name"] = loginfo["name"] + a


            if i == 0 and line.startswith("commit"):
                i = 1
                loginfo = {}
                commit,loginfo["id"] = line.split(" ")
                loginfo["info"] = ""
                loginfo["project"] = "ZEUS"
        
        if i == 1 :
            infos.append(loginfo)
        f.close()

        self.tStatistics.write("""
            <br></br>
            <br></br>
            <table border="0" cellpadding="5"  align=center  cellspacing="2" width="95%">            
            <tr align="center" bgcolor="#000800" height="10px" style="color:white"><th> commit </th></tr>
            </table>
            <table  border="0" cellpadding="5"  align=center  cellspacing="2" width="95%">            
            <tr><th>i</th><th>module</th><th>id</th><th>time</th><th>message</th><th>name</th><th>email</th></tr>
            """)
        i = 1
        for f in infos:
            print f
            f["email"] = f["email"].replace("<","")
            f["email"] = f["email"].replace(">","")
            self.tStatistics.write("<tr><td>" +  str(i) + "</td><td>" + f["project"] + "</td><td>"+f["id"] + "</td><td>" + f["year"] + "-" + f["month"] + "-"+ f["day"] + "-"+ f["time"] + "</td><td>" + f["info"] + "</td><td>" + f["name"] + "</td><td>" + f["email"] + "</td></tr>")
            
            i = i + 1
        self.tStatistics.write("</table>")
    
    
    def createchangelog(self):
        if os.path.exists(".\\gitchangelog.txt"):
            print "[createReport] find the gitchangelog.txt "
            self.getchangelog()
        else:
            print "[createReport] do not find the gitchangelog"
