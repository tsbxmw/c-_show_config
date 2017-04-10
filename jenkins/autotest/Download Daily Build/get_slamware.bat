:: version : 1.2
:: get the daily slamware from the windows share directory
:: sdp slamware daily build
:: author : wei.meng
:: modify : 2017.2.20 - add the env SLAMWARE_PATH

echo off

:: the day : today
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
set today=%year%%month%%day%

:: the path part not change
set slamware_path_not_change=%SLAMWARE_PATH%

:: the rom file
set slamware_name_pre=zeus_edison.2.2.1_rtm
set slamware_name_end=bin
set slamware_name=%slamware_name_pre%.%today%.%slamware_name_end%

:: the path 
set slamware_path=%slamware_path_not_change%\%today%

:: the local path : save the slamware 

set slamware_local=..\testdata\sdprprom\today

:: delete the local path files
:: echo Y | del %slamware_local%\*

if exist %slamware_path%\%slamware_name%  (
	 echo find the %slamware_name% ! 
     echo find > .\report\report.html 
     ) else (
	echo fail to get the %slamware_name%
    echo don't find > .\report\report.html
	exit 1
)


:: get the slamware to the local directory

robocopy  %slamware_path% %slamware_local% %slamware_name%

if exist %slamware_local%\%slamware_name%  (
    echo get the %slamware_name% successful! 
    echo "copy successful" > .\report\report.html 
    exit 0
     ) else (
    echo fail to get the %slamware_name%
    echo "copy Failed" > .\report\report.html
	exit 1
)




::if exist report  ( 
  ::  echo "copy successful" > .\report\report.html
    ::) else (
    ::md report 
    ::echo "copy successful" > .\report\report.html
::)
    

pause

