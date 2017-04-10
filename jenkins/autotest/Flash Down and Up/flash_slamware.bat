:: version : 1.0
:: flash the daily version to the sdp or zues
:: sdp slamware daily build
:: author : wei.meng
:: modify : 2017.2.20 - add the env SLAMWARE_PATH
:: modify : 2017.2.23 - add the env IP_SLAMWARE -- using update.py as new file
:: modify : 2017.2.27 - add today to the slamware_local
:: modify : 2017.2.28 - add down an up -- add COUNT_OF_DOWNUP
:: modify : 2017.3.01 - change to slamware_name_pre\date\end\num_old -- add python checkversoin
:: modify : 2017.3.02 - test - add the test date = 20170302 -- when the version is wrong , exit with 1
:: modify : 2017.3.09 - add the down and up dir to save the build file 
:: 2.3.0_dev-zeus-20170122

@echo off

:: the day : today
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
set today=%year%%month%%day%

:: test define
set today=20170302
  
set path_here=%CD%

cd ..
set path_father=%CD%

cd %path_here%

:: the rom file today , if you change the version rules , please change the set below
:: rules : zeus_edison.2.2.1_rtm.20170301.bin
::         pre        . num     . date   . end

set slamware_name_pre=zeus_edison
set slamware_name_num=2.2.1_rtm
set slamware_name_end=bin

set slamware_name=%slamware_name_pre%.%slamware_name_num%.%today%.%slamware_name_end%

:: the rom file old at the dir ..\testdata\sdprprom\old , old file if changed , the below changed 
:: use the old firmware to downgrade the version
:: now is zeus_edison.2.2.1_rtm.20170228.bin

set slamware_name_pre_old=zeus_edison
set slamware_name_num_old=2.2.1_rtm
set slamware_name_date_old=20170228
set slamware_name_end_old=bin


set slamware_name_old=%slamware_name_pre_old%.%slamware_name_num_old%.%slamware_name_date_old%.%slamware_name_end_old%

:: the local path : today slamware path
set slamware_local=testdata\sdprprom\up
:: the local path : old slamware path
set slamware_local_old=testdata\sdprprom\down

:: update the firmware

if exist ..\%slamware_local%\%slamware_name%  (
 echo local version file was downloaded ) else (
 echo do not find the file %slamware_name% at %slamware_local% 
 exit 1
    )
if exist ..\%slamware_local_old%\%slamware_name_old%  (
 echo old version file was finded ! ) else (
 echo do not find the file %slamware_name_old% at %slamware_local_old% 
 exit 1
    )

:: add flash code below 
:: update.py is using to upgrade or downgrade the version
:: checkversion.py is using to check the version of the sdp and the bin file version 
:: everytime using the update.py ,the checkversion.py would be useful
:: 10.16.130.63
echo ---------------------------
echo    ALL : %COUNT_OF_DOWNUP%
echo ---------------------------
for /l %%i in (1,1,%COUNT_OF_DOWNUP%) do (
    echo ***********************************************************
    echo time : %%i
    echo ---------------------------
    echo DownGrade now ...
    python update.py  %IP_SLAMWARE%  %path_father%\%slamware_local_old%\%slamware_name_old%
    python checkversion.py %IP_SLAMWARE% %slamware_name_old%
    findstr /r success ".\\compare" > null
    if %errorlevel%==1 exit 1
    if %errorlevel%==0 echo ---------------
    
    echo ---------------------------
    echo UpGrade now ...
    python update.py  %IP_SLAMWARE%  %path_father%\%slamware_local%\%slamware_name%
    python checkversion.py %IP_SLAMWARE% %slamware_name%
    findstr /r success ".\\compare" > null
    if %errorlevel%==1 exit 1
    if %errorlevel%==0 echo ---------------
)


if exist report  ( 
    echo "flash successful" > .\report\report.html
    ) else (
    md report 
    echo "flash successful" > .\report\report.html
)




pause

