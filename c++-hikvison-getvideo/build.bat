@echo off

echo Loading the vs2010 environment...
call "%VS100COMNTOOLS%\..\..\VC\vcvarsall.bat" x86\

echo Set the environment variable...
set SCRIPT_ROOT=%~dp0
set SDK_ROOT=%SCRIPT_ROOT%
set BUILD_ROOT=%SDK_ROOT%


echo Building slamware sdk test...

set WORKSPACE_ROOT=%SDK_ROOT%

msbuild test.sln 