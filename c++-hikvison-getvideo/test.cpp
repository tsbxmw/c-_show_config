#include "stdafx.h"
using namespace std;

typedef HWND (WINAPI *PROCGETCONSOLEWINDOW)();
LONG lPort;

void CALLBACK g_ExceptionCallBack(DWORD dwType, LONG lUserID, LONG lHandle, void *pUser)
{
    char tempbuf[256] = {0};
    switch(dwType)
    {
    case EXCEPTION_RECONNECT: //预览时重连
        printf("----------reconnect--------%d\n", time(NULL));
        break;
    default:
        break;
    }
}
void main(int argc, char **args)
{
    string ip;
    string user;
    string pass;
    string filename;
    if (argc > 4)
    {
        ip = args[1];
        user = args[2];
        pass = args[3];
        filename = args[4];
    }
    else
    {
        cout << "wrong with argc , check it " << endl;
        return;
    }
    NET_DVR_Init();
    NET_DVR_SetConnectTime(2000, 1);
    NET_DVR_SetReconnect(10000, true);

    LONG IUserID;
    NET_DVR_DEVICEINFO_V30 struDeviceInfo;
    IUserID = NET_DVR_Login_V30(args[1],8000,args[2],args[3],&struDeviceInfo);
    //IUserID = NET_DVR_Login_V30("10.16.129.14",8000,"admin","Admin123",&struDeviceInfo);
    if (IUserID < 0 )
    {
        cout << " login error check the error " << NET_DVR_GetLastError() << endl;
        NET_DVR_Cleanup();
        return;
    }
    else{
        cout << " login successful ! " << endl;

    }

    NET_DVR_SetExceptionCallBack_V30(0, NULL,g_ExceptionCallBack, NULL);

    NET_DVR_PREVIEWINFO struPlayInfo = {0};
    HWND hWnd = GetConsoleWindow(); 
    struPlayInfo.hPlayWnd = NULL; //需要 SDK 解码时句柄设为有效值，仅取流不解码时可设为空
    struPlayInfo.lChannel = 1; //预览通道号
    struPlayInfo.dwStreamType = 0; //0-主码流，1-子码流，2-码流 3，3-码流 4，以此类推
    struPlayInfo.dwLinkMode = 4; //0- TCP 方式，1- UDP 方式，2- 多播方式，3- RTP 方式，4-RTP/RTSP，5-RSTP/HTTP
    struPlayInfo.bBlocked = 1; //0- 非阻塞取流，1- 阻塞取流
 

    LONG lRealPlayHandle;
    lRealPlayHandle = NET_DVR_RealPlay_V40(IUserID,&struPlayInfo, NULL,NULL);
    cout << NET_DVR_GetLastError() << endl;
    if(lRealPlayHandle < 0)
    {

        cout << "Play Error " << NET_DVR_Logout(IUserID) << endl;
        NET_DVR_Cleanup();
        return;
    }
    if (NET_DVR_SaveRealData(lRealPlayHandle,args[4]))
    {
        cout << "start recording now.... " << endl;
    }
    while(true);
    NET_DVR_StopRealPlay(lRealPlayHandle);
    NET_DVR_Logout(IUserID);
    NET_DVR_Cleanup();
    return;

    

}
