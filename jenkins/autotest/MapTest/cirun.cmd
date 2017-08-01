if not exist log ( md log )
if not exist report ( md report )
if not exist json ( md json )
python maptest.py %IP_SLAMWARE% maps\map.stcm mapdownload\map.stcm