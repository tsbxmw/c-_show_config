:: get the one build bin file
:: author : wei.meng @ slamtec.inc
:: date : 20170309
:: version : 1.0

echo ------------------------------
echo [get the one build bin file ]
set downbuildpath=%NAME_OF_DOWNBUILD%
echo the path is %downbuildpath%
set localpath=..\\testdata\\down\\
xcopy /yse %downbuildpath% %localpath%
echo ------------------------------
echo [get the one build bin file ]
set upbuildpath=%NAME_OF_UPBUILD%
echo the path is %upbuildpath%
set localpath=..\\testdata\\up\\
xcopy /yse %upbuildpath% %localpath%
echo ------------------------------