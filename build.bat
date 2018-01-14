echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\testshow\c++-GetH264FromRtsp\GetH264FromRtsp.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\testshow\c++-getkeydown-background\getkeydown.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\testshow\c++-hikvison-getvideo\test.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

