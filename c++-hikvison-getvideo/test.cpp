#include "stdafx.h"
using namespace std;

typedef HWND (WINAPI *PROCGETCONSOLEWINDOW)();
LONG lPort;

void CALLBACK g_ExceptionCallBack(DWORD dwType, LONG lUserID, LONG lHandle, void *pUser)
{
    char tempbuf[256] = {0};
    switch(dwType)
    {
    case EXCEPTION_RECONNECT: //Ԥ��ʱ����
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
    struPlayInfo.hPlayWnd = NULL; //��Ҫ SDK ����ʱ�����Ϊ��Чֵ����ȡ��������ʱ����Ϊ��
    struPlayInfo.lChannel = 1; //Ԥ��ͨ����
    struPlayInfo.dwStreamType = 0; //0-��������1-��������2-���� 3��3-���� 4���Դ�����
    struPlayInfo.dwLinkMode = 4; //0- TCP ��ʽ��1- UDP ��ʽ��2- �ಥ��ʽ��3- RTP ��ʽ��4-RTP/RTSP��5-RSTP/HTTP
    struPlayInfo.bBlocked = 1; //0- ������ȡ����1- ����ȡ��
 

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
