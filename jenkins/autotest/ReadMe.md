*************************************
* version : 1.2
* date    : 20170310
* author  : wei.meng
* copyright : slamtec.inc
*************************************
* modify : 20170320 - change to md file
* modify : 20170426 - add move and check test

*************************************

# ReadMe.md

> First of all ,before using the code of the test, please read the ReadMe.txt first.

## 1, base :
   
>    the tools and other files

    base
    |- tools :
    |- pylibs - including the SSH , Update , Flash ,Check mode etc...
        |- win32tools - some dll or lib or exe or etc...
             |- zeustool.exe - zeus tool of some function ...

## 2, Flash Daily Build :

>    using the daily build to upgrade the device firmware
    
    Flash Daily Build
    |- report : the report of the stage Flash Daily Build
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script  to flash the slamware 
    |- flash_slamware.py : replace the flash_slamware.bat 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...
    
## 3, Flash Down and Up :
    
>    using the down and up build to test the downgrade and upgrade slamware

    Flash Down and Up
    |- report : the report of the stage Flash Down and Up
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script to flash the slamware which is writed by bat script
    |- flash_slamware.py : the new script using to replace the old 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...
    
## 4, Flash One Build :

>    using one build to test the slamware upgrade

    Flash One Build
    |- report : the report of the stage Flash One Build
    |- cirun.cmd : the pipeline would run this cmd on windows
    |- flash_slamware.bat : the old script to flash the slamware which is writed by bat script
    |- flash_slamware.py : the new script using to replace the old 
    |- sdkconnect.exe : test the sdk connect with the zeus or sdk ...

## 5, GoHome Test :

>   sing the auto.exe to test the gohome of the zeus

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

    