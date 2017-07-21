
echo ------------------------------------------------------
call getinfo.exe %DEVICE_IP%
echo ------------------------------------------------------
echo start test
echo ALL : %COUNT_OF_TEST%
echo POINT : ( %POINT_X% , %POINT_Y% )
call auto.exe -t %DEVICE_IP%  test5 %COUNT_OF_TEST%  %POINT_X%  %POINT_Y%
echo test end !
echo ------------------------------------------------------