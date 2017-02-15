
#include<iostream>
#include<string>
#include<rpos\robot_platforms\slamware_core_platform.h>
#include<rpos\features\sweep_motion_planner.h>
#include "bitmap.h"
#include <Windows.h>
#include "Source.h"

using namespace std;
using namespace rpos::robot_platforms;
using namespace rpos::core;
using namespace rpos::features;
using namespace rpos::actions;
using namespace rpos::features::detail;
using namespace rpos::features::system_resource;




void main()
{
    while(true)
    {

        try{

            string ipaddress_station = "10.16.130.78";
            string ipaddress_apmode = "192.168.11.1";
            string ipadd;

            int port = 1445;
            int timeout = 60000;
            int flag = 0;
            int exitcode = 0;
            string ccmd = "-1";
            int cmd = -1;
            int choose = 1;
            string input = "y";
            SlamwareCorePlatform platform ;
            map<string,int> cmap;
            cmap = MapInit(cmap);

            cout << " -------------------------------------------------------------" << endl;

            while(true)
            {
                cout << " input ip or not (y/n) : " ;
                cin >> input;

                if (input == "yes" || input == "y" || input == "Y" || input == "YES" )
                {
                   
                    while(true)
                    { 
                        cout << " SDP IP (:1445) : " ;
                        cin >> ipadd;
                        
                        try{
                             platform = init(ipadd,port,timeout);
                             if(platform)
                                 break;
                        }catch(rpos::robot_platforms::ConnectionFailException &e)
                        {
                            cout << " connection fail " << e.what() << endl;
                            continue;
                
                        } catch (rpos::system::detail::ExceptionBase & e) {
                            cout << " fail on " << e.what() << endl;
                            continue;
                        }
                    }
                    break;
                }
                else if (input == "no" || input == "n" || input == "N" || input == "NO")
                {

                    cout << " [1] station SDP IP (:1445) : " << ipaddress_station << endl; 
                    cout << " [2] apmode  SDP IP (:1445) : " << ipaddress_apmode << endl;
                    
                    while( true )
                    {
                        cout << " choose : " ;
                        cin >> choose;
                        if(choose == 1)
                        {
                            cout << " connect to " << ipaddress_station << " : 1445 " << endl;
                            ipadd = ipaddress_station;
                            try{
                                 platform = init(ipadd,port,timeout);
                                 if(platform)
                                     break;
                            }catch(rpos::robot_platforms::ConnectionFailException &e)
                            {
                                cout << " connection fail " << e.what() << endl;
                                continue;
                
                            } catch (rpos::system::detail::ExceptionBase & e) {
                                cout << " fail on " << e.what() << endl;
                                continue;
                            }
                        }
                        else if(choose == 2)
                        {
                            cout << " connect to " << ipaddress_apmode << " : 1445 " << endl;
                            ipadd = ipaddress_apmode;
                            try{
                                 platform = init(ipadd,port,timeout);
                                 if(platform)
                                     break;
                            }catch(rpos::robot_platforms::ConnectionFailException &e)
                            {
                                cout << " connection fail " << e.what() << endl;
                                continue;
                
                            } catch (rpos::system::detail::ExceptionBase & e) {
                                cout << " fail on " << e.what() << endl;
                                continue;
                            }
                        }
                        else
                        {
                            cout << " wrong input , try again " << endl;
                            cout << " choose : " ;
                        }
                    }
                    break;
                }
                else{
                    cout << " wrong input , try again " << endl;
                    cout << " input ip or not (y/n) : " ;
                }
            }
            cout << " connect successful ! " << endl;
            

            cout << " -------------------------------------------------------------" << endl;
            

            while(platform)
            {

                flag = 1;
                cout << "  -------------------------------------------------------------  " << endl;
                cout << " |        connect to  " <<  ipadd  << ":1445 " << endl
                     << " |  -1 : help ?       0 : moveto      1 : addwall              | " << endl 
                     << " |   2 : clearwalls   3 : addwalls    4 : exit                 | " << endl
                     << " |   5 : gohome       6 : turn left   7 : turn right           | " << endl
                     << " |   8 : set network  9 : deviceinfo 10 : robot station        | "<< endl
                     << " |  11 : map info    12 : laser scan 13 : get walls            | " << endl
                     << " |  14 : add line    15 : get lines  16 : get sensor values    | " << endl
                     << " |  17 : get netinfo 18 : moveby                               | " << endl;
                cout << "  -------------------------------------------------------------  " << endl;
                cout << " cmd (number) :";
                cin >> ccmd;


                int timeflagm = 0;
        
                
                switch(cmap.count(ccmd) ? cmap[ccmd] : -1){
                
                case -1 :
                    Helpinfo();
                    break;

                case 0 :
                    Moveto_xy(platform);
                    break;

                case 1 :
            
                    AddWall(platform);
                    break;

                case 2 :
                    cout << " clear walls now ... " << endl;
                    platform.clearWalls();
                    break;

                case 3 :
                    break;

                case 4 :
                    cout << " exit now .. (-_-)" << endl;
                    platform.disconnect();
                    exitcode = 1;
                    break;

                case 5 :
                    GoHome(platform);
                    break;

                case 6 :
                    TurnLeft(platform);
                    break;

                case 7 :
                    TurnRight(platform);
                    break;

                case 8 :
                    SetNetwork(platform);
                    break;

                case 9:
                    GetDeviceInfo(platform);
                    break;

                case 10:
                    ShowSystemInfo(platform);

                    break;

                case 11:
                    SaveMAPtoBMP(platform);
                    break;

                case 12 :
                    LaserScanShow(platform);
                    break;

                case 13 :
                    GetWalls(platform);
                    break;

                case 14:
                    AddLine(platform);
                    break;

                case 15:
                    GetAllLines(platform);
                    break;
          
                case 16:
                    GetSensorValues(platform);
                    break;

                case 17:
                    GetNetworkInfo(platform);
                    break;

                case 18:
                    MoveBy(platform);
                    break;

                default:
                    cout << " wrong input ! try again ! " << endl;
                    break;
                }
                if(exitcode == 1)
                    break;
            }

    
         
        }
        catch (rpos::robot_platforms::ConnectionFailException &e)
        {
            cout << " connection fail " << e.what() << endl;
        }
        catch (rpos::system::detail::ExceptionBase & e) {
            cout << " fail on " << e.what() << endl;
        }
    }
}