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
:: 2.3.0_dev-zeus-20170122 
:: modify : 2017.3.3 - change to flash one buil times
:: zeus_deison.2.3.0_dev.20170122
:: zeus_edison.2.2.1_rc4.20170217.bin
:: zeus_edison.2.2.1_rtm.20170228.bin

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

:: the rom file today , if you change the version rules , please change the set below
:: rules : zeus_edison.2.2.1_rtm.20170301.bin
::         pre        . num     . date   . end

::set slamware_name_pre=zeus_edison
::set slamware_name_num=2.2.1_rtm
::set slamware_name_end=bin

::set slamware_name=%slamware_name_pre%.%slamware_name_num%.%today%.%slamware_name_end%

:: split the path
set pathofslamware=%NAME_OF_ONEBUILD%

set slamware_name=%

:: the local path : today slamware path
set slamware_local=testdata\sdprprom\oneday

:: update the firmware

if exist ..\%slamware_local%\%slamware_name%  (
 echo local version file was downloaded ) else (
 echo do not find the file %slamware_name% at %slamware_local% 
 exit 1
    )

:: add flash code below 
:: update.py is using to upgrade or downgrade the version
:: checkversion.py is using to check the version of the sdp and the bin file version 
:: everytime using the update.py ,the checkversion.py would be useful
:: 10.16.130.63
echo ---------------------------
echo    ALL : %COUNT_OF_ONEBUILD%
echo ---------------------------
for /l %%i in (1,1,%COUNT_OF_ONEBUILD%) do (
    echo ***********************************************************
    echo time : %%i
    echo ---------------------------
    echo UpGrade now ...
    python update.py  %IP_SLAMWARE%  %path_father%\%slamware_local%\%slamware_name%
    python checkversion.py %IP_SLAMWARE% %NAME_OF_ONEBUILD%
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

