/*
* 功能 ： API 测试
* 测试类 ： RobotPlatform
* 时间 ： 20170209
*/


#define Pi 3.1415926

#include<iostream>
#include<string>
#include<rpos\robot_platforms\slamware_core_platform.h>

using namespace rpos::robot_platforms;
using namespace rpos::core;
using namespace rpos::features;
using namespace rpos::actions;
using namespace std;

class Test_RobotPlatform{

public:

    string ipaddress;
    int port;
    SlamwareCorePlatform test_platform;

public:
    Test_RobotPlatform(string ip, int p) : ipaddress(ip) , port(p)
    {
        cout << " [ test info ] ip : port " << this->ipaddress << " : " << this->port << endl;
    }

    ~Test_RobotPlatform(){}
    // connect
    void test_init();
    // disconnect
    void test_end();
    // run all test
    void run_all_test();

    bool test_getWalls();
    bool test_addWall();
    bool test_clearWalls();

};

void Test_RobotPlatform::run_all_test()
{
    cout << " [ Start All Test ... ] " << endl << endl;
    cout << " [ ******** Test 1.1 ******** ] " << endl << endl;
    test_getWalls();
    cout << endl << " [ ######## Test 1.1 ######## ] " << endl << endl;

    cout << " [ ******** Test 2.1 ******** ] " << endl << endl;
    test_addWall();
    cout << endl << " [ ######## Test 2.1 ######## ] " << endl << endl;

    cout << " [ ******** Test 3.1 ******** ] " << endl << endl;
    test_clearWalls();
    cout << endl << " [ ######## Test 3.1 ######## ] " << endl << endl;

    cout << endl << " [ All Test Complete ... ] " << endl;

}

void Test_RobotPlatform::test_init()
{
    test_platform = SlamwareCorePlatform::connect(ipaddress,port);
    //cout << " connect successful ... " << endl;
}

void Test_RobotPlatform::test_end()
{
    test_platform.disconnect();
    //cout << " disconnected " << endl;
}

bool Test_RobotPlatform::test_getWalls()
{
    cout << " [ RobotPlatform::getWalls() ]  test start ... " << endl;
    bool test_result_getWalls = false;
    test_init();
    try{
        cout << " [ RobotPlatform::getWalls() ]  getWalls() now ... " << endl;
        if( test_platform.getWalls().size() >= 0 )
        {
            test_result_getWalls = true;
        }
        
    }catch(string x)
    {
        cout << x << endl;
    }
    finally:
        test_end();
        cout << " [ RobotPlatform::getWalls() ]  test complete  ... " << endl;
        cout << " [ RobotPlatform::getWalls() ]  test result : " << test_result_getWalls << endl;

    return test_result_getWalls;
}






bool Test_RobotPlatform::test_addWall()
{
    cout << " [ RobotPlatform::addWall() ]  test start ... " << endl;
    bool test_result_addWall = false;
    test_init();

    if( test_clearWalls() )
    {
        cout << " [ RobotPlatform::addWall() ]  addWall _ Line(Point(0,0),Point(10000000,10000000)) _ now ... " << endl;
        assert(test_platform.addWall(Line(Point(0,0),Point(10000000,10000000))));
 
        assert( !test_platform.getWalls().empty() );
        std::vector<Line> result = test_platform.getWalls();

        cout << " [ RobotPlatform::addWall() ]  check Wall _ Line(Point(0,0),Point(10000000,10000000)) _ now ... " << endl;
        if ( result.at(0).startP().x() == 0 && result.at(0).startP().y() == 0 
                    && result.at(0).endP().x() == 10000000 && result.at(0).endP().y() == 10000000 )
        {
                    test_result_addWall = true;
        }

    }
    finally:
        test_end();
        cout << " [ RobotPlatform::addWall() ]  test complete ... " << endl;
        cout << " [ RobotPlatform::addWall() ]  test result : " << test_result_addWall << endl;
    return test_result_addWall;
}



bool Test_RobotPlatform::test_clearWalls()
{
    cout << " [ RobotPlatform::clearWalls() ]  test start ... " << endl;
    bool test_result_clearWalls = false;
    if( test_getWalls() )
    {
        test_init();

        cout << " [ RobotPlatform::clearWalls() ]  clearWalls now ... " << endl;
        if (test_platform.clearWalls())
        {
            cout << " [ RobotPlatform::clearWalls() ]  check getWalls result is NULL ... " << endl;
            if( test_platform.getWalls().empty())
            {
               test_result_clearWalls = true;
            }
        }

      
    }
    finally:
          test_end();
          cout << " [ RobotPlatform::clearWalls() ]  test complete ... " << endl;
          cout << " [ RobotPlatform::clearWalls() ]  test result :  " << test_result_clearWalls << endl;
    return test_result_clearWalls;
}