*************************************
* version : 1.4
* date    : 20170310
* author  : wei.meng
* copyright : slamtec.inc
*************************************
* modify : 20170320 - change to md file
* modify : 20170426 - add move and check test
* modify : 20170525 - add downgrade version test
* modify : 20170607 - delete the report log dir in the stages
*************************************

# ReadMe.md

> Before using the code of the test, please read the ReadMe.txt first.

## 1, base :
   
>    the tools and other files

    base
    |- tools :
        |- pylibs - including the SSH , Update , Flash ,Check mode etc...
        |- win32tools - some dll or lib or exe or etc...
            |- zeustool.exe - zeus tool of some function ...
            |- debugtool.exe - using to into debug mode
            |- openssl - openssl tool,compile to windows
        |- config - the version info config file here
        
    |- script :
        |- jenkins - the pipeline file of ZEUS_AUTOTEST
        |- jenkins_build - the pipeline file of RUN_BUILD


## 2, Flash Daily Build :

>    using the daily build to upgrade the device firmware
    
    Flash Daily Build    
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script  to flash the slamware 
    |- flash_slamware.py : replace the flash_slamware.bat 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...
    
## 3, Flash Down and Up :
    
>    using the down and up build to test the downgrade and upgrade slamware

    Flash Down and Up
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script to flash the slamware which is writed by bat script
    |- flash_slamware.py : the new script using to replace the old 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...

### 3.1 , Flash Wrong Build :

> using the wrong build or should not be downgrade version to test

    Flash Wrong Build:
    | - cirun.cmd : the pipeline script would run this cmd on windows
    | - flash_slamware.bat : the old script of bat
    | - flash_slamware.py : ths new script of python
    | - sdkconnect.exe : using to check the slamware up or down
    
## 4, Flash One Build :

>    using one build to test the slamware upgrade

    Flash One Build
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script to flash the slamware which is writed by bat script
    |- flash_slamware.py : the new script using to replace the old 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...

## 5, GoHome Test :

>   using the auto.exe to test the gohome of the zeus

    GoHome Test
    |- auto.exe : the program to run the test with some inputs
    
## 6, Send Report :

>    using to publish the report.html to the jenkins and copy the report files to the windows-share-dir

    Send Report
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- createreport.py : create the report summary.html 
   
## 7, Simulator Mode :

>    using to get the device into the simulator mode

    Simulator Mode
    |- report : the report of the stage Simulator Mode
    |- cirum.cmd : the pipeline of the stage Simulator Mode
    |- debugmode.py : get the device into the simulator mode
    |- SSH.py : already moved to the base/tools/pylibs dir
   
## 8, MoveTest

>    using to test the zeus move and check the moveaction

    MoveTest
    |- report : the report of the stage MoveTest Mode
    |- cirum.cmd : the pipeline of the stage MoveTest Mode
    |- config.config : the config file of move test
    |- movetest.py : the script of movetest
    |- moveandcheck.exe : the tool of move and check
    


## 9, testdata :

>    using to save the test log / slamware / report or etc...

    testdata
    |- mapjson : the Simulator Mode would use the json and map files
    |- report : save the all stage report here
        |- json : save the all stage report json file here
    |- sdrprom : save the build_files here
          |- old : the old slamware
          |- oneday : the one-day build
          |- up : the up build
          |- down : the down build
          |- today : today build


--------

## How to use it ?

> 1 , create a jenkins pipeline job .

    example : http://jenkins.slamtec.com/ZEUS_AUTOTEST

> 2 , using the pipeline file in the script.

    u can just copy it to the pipeline script , or
    using git to checkout it and use it.

> 3 , build the job .

    u must define the parameters in the pipeline job , if not , the test script would crash sometimes.

> 4 , modify the pipeline and test script to suit your test

    the pylibs and win32tools and the scripts in the stage directory should be modified before using it.