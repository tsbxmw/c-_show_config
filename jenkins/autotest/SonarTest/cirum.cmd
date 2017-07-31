if not exist log ( md log )
if not exist report ( md report )
if not exist json ( md json )
python sonartest.py %IP_SLAMWARE%