echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\c-_show_config\c++-GetH264FromRtsp\GetH264FromRtsp.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\c-_show_config\c++-getkeydown-background\getkeydown.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

echo ------------------------------------------------------------------------------------------------
msbuild "C:\projects\c-_show_config\c++-hikvison-getvideo\test.vcxproj" /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"

