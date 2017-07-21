if not exist log ( md log )
if not exist report ( md report )
if not exist json ( md json )
set IP_SLAMWARE=10.16.130.129
python sonartest.py %IP_SLAMWARE%