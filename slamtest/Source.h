/*
  Source.h
  all functions here 
*/


#include<iostream>
#include<string>
#include<rpos\robot_platforms\slamware_core_platform.h>
#include<rpos\features\sweep_motion_planner.h>
#include "bitmap.h"
#include <Windows.h>

#define Pi 3.1415926

using namespace std;
using namespace rpos::robot_platforms;
using namespace rpos::core;
using namespace rpos::features;
using namespace rpos::actions;
using namespace rpos::features::detail;
using namespace rpos::features::system_resource;




SlamwareCorePlatform init(string ipaddress,int port,int timeout)
{
    SlamwareCorePlatform platform;
    try{
        platform = SlamwareCorePlatform::connect(ipaddress,port,timeout);
    }
    catch(rpos::system::detail::ExceptionBase &e)
    {
        std::cout << " fail with " << e.what() << endl;
    }
    return platform;
}

map<string,int> MapInit(map<string,int> cmap)
{
    int size = 20;
    string a[100] = {"-1","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"};
    int b[100] = {-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
    for(int i = 0; i < size; i++)
    {
        cmap[a[i]] = b[i];
        
    }
    return cmap;
}

void teardown(SlamwareCorePlatform platform)
{
    platform.disconnect();
}


void Helpinfo()
{
    cout << " ----------------------------------------------------------------------------" << endl;
    cout << " cmd : " << endl
        << "  -1 : help ?           show help info " << endl
        << "   0 : moveto           move to point ( x , y )" << endl 
        << "   1 : addwall          add wall ( x1,y1 ) ( x2,y2 )" << endl 
        << "   2 : clearwalls       clear all walls" << endl
        << "   3 : addwalls (*)                 " << endl
        << "   4 : exit             exit now ..." << endl
        << "   5 : gohome           go home and charging" << endl
        << "   6 : turn left        turn left ( 逆时针转动 ） time (s)" << endl
        << "   7 : turn right       turn left ( 顺时针转动 ） time (s)" << endl
        << "   8 : network          connect to new network (ssid , password)" << endl
        << "   9 : device info      show device info " << endl
        << "  10 : robot station    show system info "<< endl
        << "  11 : map info         save map to a MAP.bmp file" << endl
        << "  12 : laser scan       show laser scan result " << endl
        << "  13 : get walls        get all walls info " << endl
        << "  14 : add line         add line ( x1,y1 ) ( x2,y2 )" << endl
        << "  15 : get lines        get all lines info " << endl
        << "  16 : get sensorvalues get all sensors' values and time " << endl
        << "  17 : get netinfo      get ssid and mode of network " << endl
        << "  18 : moveby           move to the direction " << endl
        << " cmd : ";
    cout << " ----------------------------------------------------------------------------" << endl;
}

void Moveto_xy(SlamwareCorePlatform platform)
{
    try{
    double x1,y1;
    cout << " input the location (double x, double y) : " ;
    cin >> x1 >> y1;
    cout << " move to ( " << x1 << "," << y1 << " )" << endl;
    Location location = Location(x1,y1);
    MoveAction moveaction = platform.moveTo(location,true,true);
    motion_planner::Path path = moveaction.getRemainingPath();
    vector<Location> points = path.getPoints();
    double x ,y ,z ,yaw ,pitch ,roll;
    int flag = 1;
    x = platform.getLocation().x();
    y = platform.getLocation().y();
    z = platform.getLocation().z();
    yaw = platform.getPose().yaw() * 180 / Pi;
    pitch = platform.getPose().pitch();
    roll = platform.getPose().roll();
    
    cout << " actionId : " << moveaction.getActionId() << " actionName : " << moveaction.getActionName() << endl;
        
    for(vector<Location>::const_iterator it = points.begin(); it != points.end() ; it++ )
        cout <<  " [ " << it->x() << " , " << it->y() << " ] " << endl;

    while(moveaction){
        if (flag == 1)
        {
            _sleep(2000);
            flag = 0;
        }
        if ( x == platform.getLocation().x() && y == platform.getLocation().y() && z == platform.getLocation().z() &&  yaw == platform.getPose().yaw() &&
            pitch == platform.getPose().pitch() && roll == platform.getPose().roll())
        {
            break;
        }
        else
            cout << " Pose : " << x << "  " << y << "  " << z << "  " << yaw * 180 / Pi << "  " << pitch << "  " << roll << endl;
        _sleep(50);
        x = platform.getLocation().x();
        y = platform.getLocation().y();
        z = platform.getLocation().z();
        yaw = platform.getPose().yaw();
        pitch = platform.getPose().pitch();
        roll = platform.getPose().roll();
    }
    } catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }
}

void SaveMAPtoBMP(SlamwareCorePlatform platform)
{
    try{
    cout << " get map and save to bmp " << endl;
    rpos::core::RectangleF knownArea = platform.getKnownArea(location_provider::MapTypeBitmap8Bit, rpos::features::location_provider::EXPLORERMAP);
    location_provider::Map map = platform.getMap(location_provider::MapTypeBitmap8Bit, knownArea, rpos::features::location_provider::EXPLORERMAP);
    std::string finalFilename = "Map";
    finalFilename += ".bmp";
    bitmap_image mapBitmap(map.getMapDimension().x(), map.getMapDimension().y());

    for (size_t posY = 0; posY < map.getMapDimension().y(); ++posY)
    {
        for (size_t posX = 0; posX < map.getMapDimension().x(); ++posX)
        {
            rpos::system::types::_u8 cellValue = ((rpos::system::types::_u8)128U) + map.getMapData()[posX + (map.getMapDimension().y()-posY-1) * map.getMapDimension().x()];
            mapBitmap.set_pixel(posX, posY, cellValue, cellValue, cellValue);
        }
    }
    mapBitmap.save_image(finalFilename);
    }catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }
}

void GoHome(SlamwareCorePlatform platform)
{
    try{
    cout << " gohome now ... " << endl;
    MoveAction moveaction = platform.goHome();
    motion_planner::Path path = moveaction.getRemainingPath();
    vector<Location> points = path.getPoints();
    double x ,y ,z ,yaw ,pitch ,roll;
    int flag = 1;
    x = platform.getLocation().x();
    y = platform.getLocation().y();
    z = platform.getLocation().z();
    yaw = platform.getPose().yaw() * 180 / Pi;
    pitch = platform.getPose().pitch();
    roll = platform.getPose().roll();
    cout << " actionId : " << platform.getCurrentAction().getActionId() << " actionName : " << platform.getCurrentAction().getActionName() << endl;
        
    for(vector<Location>::const_iterator it = points.begin(); it != points.end() ; it++ )
        cout <<  " [ " << it->x() << " , " << it->y() << " ] " << endl;
    while(moveaction){
        if (flag == 1)
        {
            _sleep(2000);
            flag = 0;
        }
        if ( x == platform.getLocation().x() && y == platform.getLocation().y() && z == platform.getLocation().z() &&  yaw == platform.getPose().yaw() &&
            pitch == platform.getPose().pitch() && roll == platform.getPose().roll())
        {
            break;
        }
        else
            cout << " Pose : " << x << "  " << y << "  " << z << "  " << yaw * 180 / Pi << "  " << pitch << "  " << roll << endl;
        _sleep(50);
        x = platform.getLocation().x();
        y = platform.getLocation().y();
        z = platform.getLocation().z();
        yaw = platform.getPose().yaw();
        pitch = platform.getPose().pitch();
        roll = platform.getPose().roll();
    }
    }catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }
}

void TurnLeft(SlamwareCorePlatform platform )
{
    try{
    int timeflagm = 0;
    int time;
    SYSTEMTIME sys;
    DWORD start;
    

    cout << " input time ( s) : " ;
    cin >> time;
    cout << " start rotating (逆时针) : " << time << " s" << endl;
    GetLocalTime(&sys);
    cout << " Start time : " << sys.wYear << "/" << sys.wMonth << "/" << sys.wDay << " - " << sys.wHour << ":" << sys.wMinute << ":" << sys.wSecond << endl;
    cout << " Time (s) : 0 -> " ;
    start = GetTickCount();
    platform.rotate(Rotation(10,0,0));
    while( GetTickCount() - start < 1000 * time )
    {
        platform.rotate(Rotation(1,0,0));
    }
    platform.rotate(Rotation(0,0,0));
    cout << time << endl;
    GetLocalTime(&sys);
    cout << " Stop  time : " << sys.wYear << "/" << sys.wMonth << "/" << sys.wDay << " - " << sys.wHour << ":" << sys.wMinute << ":" << sys.wSecond << endl;
    cout << " Rotating over : " << time << " s"  << endl;
    }catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }
}

void TurnRight(SlamwareCorePlatform platform )
{
    try{
    int timeflagm = 0;
    int time;
    SYSTEMTIME sys;
    DWORD start;
   

    cout << " input time ( s) : " ;
    cin >> time;
    cout << " start rotating (顺时针) : " << time << " s" << endl;
    GetLocalTime(&sys);
    cout << " Start time : " << sys.wYear << "/" << sys.wMonth << "/" << sys.wDay << " - " << sys.wHour << ":" << sys.wMinute << ":" << sys.wSecond << endl;
    cout << " Time (s) : 0 -> " ;
    start = GetTickCount();
    platform.rotate(Rotation(-10,0,0));
    while( GetTickCount() - start < 1000 * time )
    {
        platform.rotate(Rotation(-1,0,0));
    }
    platform.rotate(Rotation(0,0,0));
    cout << time << endl;
    GetLocalTime(&sys);
    cout << " Stop  time : " << sys.wYear << "/" << sys.wMonth << "/" << sys.wDay << " - " << sys.wHour << ":" << sys.wMinute << ":" << sys.wSecond << endl;
    cout << " Rotating over : " << time << " s"  << endl;
    }catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }
}


void SetNetwork(SlamwareCorePlatform platform)
{
    try{
    string ssid,password;
    map<string,string> options;
    cout << " set network configuration " << endl;
    cout << " ssid : " ;
    cin >> ssid;
    cout << " password : " ;
    cin >> password;
    cout << endl;
    options["ssid"] = ssid;
    options["password"] = password;
    platform.configurateNetwork(NetworkModeStation,options);
    }catch(rpos::system::detail::ExceptionBase &e)
    {
        cout << " fail on " << e.what() << endl;
    }

}

void GetDeviceInfo(SlamwareCorePlatform platform)
{
    cout << " DeviceInfo --------------------- " << endl;
    DeviceInfo deviceInfo =  platform.getDeviceInfo();
    cout << " deviceID : " << deviceInfo.deviceID() << endl;
    cout << " hardwareVersion : " << deviceInfo.hardwareVersion() << endl;
    cout << " manufacturerID : " << deviceInfo.manufacturerID() << endl;
    cout << " manufacturerName : " << deviceInfo.manufacturerName() << endl;
    cout << " modelId : " << deviceInfo.modelID() << endl;
    cout << " modelName : " << deviceInfo.modelName() << endl;
    cout << " softwareVersion : " << deviceInfo.softwareVersion() << endl;
    deviceInfo.~DeviceInfo();
    cout << " DeviceInfo --------------------- " << endl;
}

void ShowSystemInfo(SlamwareCorePlatform platform)
{
    cout << " battery percentage : " << platform.getBatteryPercentage() << endl;
    cout << " sdk version : " <<  platform.getSDKVersion() << endl;
    cout << " sdp version : " << platform.getSDPVersion() << endl;
    cout << " DC is connected ? : " << platform.getDCIsConnected() << endl;
    /*cout << " update info       : *********** " << endl 
        << " current version   : " << platform.getUpdateInfo().currentVersion << endl
        << " new version       : " << platform.getUpdateInfo().newVersion << endl
        << " change log        : " << platform.getUpdateInfo().newVersionChangeLog << endl
        << " release date      : " << platform.getUpdateInfo().newVersionReleaseDate << endl
        << " ******************************* " << endl;*/
}

void LaserScanShow(SlamwareCorePlatform platform)
{
    LaserScan ls = platform.getLaserScan();
    cout << " has pose ? : " << ls.getHasPose() << endl;
    vector<LaserPoint> vlps  = ls.getLaserPoints();
    for(vector<LaserPoint>::iterator it = vlps.begin();it != vlps.end(); it++)
    {
        cout << " angle :  distance : valid : " << it->angle()  << " : " << it->distance() << " : " <<  it->valid() << endl;
    }
}

void GetWalls(SlamwareCorePlatform platform)
{
    cout << " get all walls ... " << endl;
    vector<Line> walls = platform.getWalls();
    for(vector<Line>::iterator it = walls.begin();it != walls.end(); it++)
        cout << " id : " << it->id() << " startP : ( " << it->startP().x() << " , " << it->startP().y()
             << " ) endP : ( " << it->endP().x() << " , " << it->endP().y() << " )"<< endl;
}

void AddLine(SlamwareCorePlatform platform)
{
    float px1,px2,py1,py2;
    px1 = px2 = py1 = py2 = 0;
    cout << " add line(x1,y1) (x2,y2) " << endl;
    cout << " input startP(x1,y1) endP(x2,y2) : " ;
    cin >> px1 >> py1 >> px2 >> py2;
    cout << " add line startP(" << px1 << "," << py1 
         << " ) endP(" << px2 << "," << ")" << endl;
    platform.addLine(artifact_provider::ArtifactUsageVirtualWall,Line(Point(px1,py2),Point(px2,py2)));
}

void GetAllLines(SlamwareCorePlatform platform)
{
    cout << " get ALL Lines : " << endl;
    for(vector<Line>::iterator it = platform.getLines(artifact_provider::ArtifactUsageVirtualWall).begin(); it != platform.getLines(artifact_provider::ArtifactUsageVirtualWall).end(); it++)
    cout << " StartP(" << it->startP().x() << " , " << it->startP().y() << " )" 
         << "   EndP(" << it->endP().x()   << " , " << it->endP().y()   << " )" << endl;
}

void AddWall(SlamwareCorePlatform platform)
{
    float px1,py1,px2,py2;
    px1= py1 = px2 = py2 = 0;
    cout << " add wall now ... " << endl;
    cout << " input wall x1 y1 , x2 y2 : ";
    cin >> px1 >> py1 >> px2 >> py2 ;
    cout << " add the wall : " << px1 << "," << py1 << " ---- " << px2 << "," << py2 << endl;
    platform.addWall( Line( Point(px1,py1) , Point(px2,py2) ) );
}

void GetSensorValues(SlamwareCorePlatform platform)
{
    bool flag = false;
    vector<impact_sensor::ImpactSensorInfo> sensorinfo;
    impact_sensor::ImpactSensorValue sensorvalue;
    flag = platform.getSensors(sensorinfo);
    vector<impact_sensor::impact_sensor_id_t> sensorid;
    
    for ( vector<impact_sensor::ImpactSensorInfo>::iterator it = sensorinfo.begin();it != sensorinfo.end();it++)
    {
        cout << " [ id : " << it->id ;
        cout << " kind : " << it->kind << " type : " << it->type ;
        cout << " ] pose : (roll,yaw,pitch,x,y,z) : (" << it->pose.roll() << "," << it->pose.yaw() << "," << it->pose.pitch() <<
            " - " << it->pose.x() << "," << it->pose.y() << "," << it->pose.z() << ") " << endl;
        sensorid.push_back(it->id);
        platform.getSensorValue(it->id,sensorvalue);
        cout << " sensorvalue time:" << sensorvalue.time << " value:" << sensorvalue.value  << endl;

    }
    
    /*//the getvalues functions

    vector<impact_sensor::ImpactSensorValue> sensorsvalue;
    platform.getSensorValues(sensorid,sensorsvalue);

    for(vector<impact_sensor::ImpactSensorValue>::iterator it = sensorsvalue.begin();it != sensorsvalue.end();it ++ )
    {
        cout << it->time << endl;
        cout << it->value << endl;
    }*/
}

void GetNetworkInfo( SlamwareCorePlatform platform)
{
   map<string,string> networkinfo =  platform.getNetworkStatus();
   for( map<string,string>::iterator it = networkinfo.begin();it != networkinfo.end();it++)
   {
       cout << " " << it->first << " : " << it->second << endl;
   }
}

void MoveBy(SlamwareCorePlatform platform)
{
    cout << " move by （direction : 0-forward 1-backward 2-turnright 3-turnleft ) : " ;
    int direction;
    cin >> direction;
    motion_planner::MoveOptions moveoptions;
    switch(direction){
    case 0 :
        platform.moveBy(rpos::core::FORWARD,moveoptions);
        break;
    case 1:
        platform.moveBy(rpos::core::BACKWARD,moveoptions);
        break;
    case 2:
        platform.moveBy(rpos::core::TURNRIGHT,moveoptions);
        break;
    case 3:
        platform.moveBy(rpos::core::TURNLEFT,moveoptions);
        break;
    default:
        cout << " wrong input " << endl;
        break;
    }


}

