:: get the one build bin file
:: author : wei.meng @ slamtec.inc
:: date : 20170309
:: version : 1.0

echo ------------------------------
echo [get the one build bin file ]
set onebuildpath=%NAME_OF_ONEBUILD%
echo the path is %onebuildpath%
set localpath=..\\testdata\\oneday\\
xcopy /yse %onebuildpath% %localpath%
echo ------------------------------
