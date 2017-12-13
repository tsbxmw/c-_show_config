echo Loading the vs2010 environment...
call "%VS100COMNTOOLS%\..\..\VC\vcvarsall.bat" x86

echo Set the environment variable...
set SCRIPT_ROOT=%~dp0
set SDK_ROOT=%SCRIPT_ROOT%
set BUILD_ROOT=%SDK_ROOT%


echo Building get video from hikivision test...

set WORKSPACE_ROOT=%SDK_ROOT%

msbuild test.vcxproj /t:Build /p:Configuration=Debug