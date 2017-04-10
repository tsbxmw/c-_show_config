:: version : 1.0
:: flash the daily version to the sdp or zues
:: sdp slamware daily build
:: author : wei.meng
:: modify : 2017.2.20 - add the env SLAMWARE_PATH
:: modify : 2017.2.23 - add the env IP_SLAMWARE -- using update.py as new file
:: modify : 2017.2.27 - add today to the slamware_local
:: modify : 2017.3.01 - add the slamware_name_end\pre\num -- add python checkversion
:: modify : 2017.3.09 - add the local env

@echo off

:: the day : today
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
set today=%year%%month%%day%

set path_here=%CD%

cd ..
set path_father=%CD%

cd %path_here%

:: the rom file
set slamware_name_pre=zeus_edison
set slamware_name_num=2.2.1_rtm
set slamware_name_end=bin
set slamware_name=%slamware_name_pre%.%slamware_name_num%.%today%.%slamware_name_end%

:: the local path : save the slamware 
set slamware_local=testdata\sdprprom\today

:: update the firmware

if exist ..\%slamware_local%\%slamware_name%  (
 echo local version file was downloaded ) else (
 echo do not find the file %slamware_name% at %slamware_local% 
 exit 1
    )

:: add flash code blow

echo UPDATE now ...

python update.py  %IP_SLAMWARE%  %path_father%\%slamware_local%\%slamware_name%

:: check update version

python checkversion.py %IP_SLAMWARE% %slamware_name%

findstr /r success ".\\compare" > null
if %errorlevel%==1 exit 1
if %errorlevel%==0 echo ---------------


if exist report  ( 
    echo "flash successful" > .\report\report.html
    ) else (
    md report 
    echo "flash successful" > .\report\report.html
)
    

pause

