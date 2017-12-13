msbuild "C:\projects\c-show-config\c++-getkeydown-background\getkeydown.sln" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\c-show-config\c++-GetH264FromRtsp\GetH264FromRtsp.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\c-show-config\c++-getkeydown-background\getkeydown.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
cd c++-hikvison-getvideo
call build.bat