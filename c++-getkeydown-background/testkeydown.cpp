#include<iostream>
#include<windows.h>

#define KEY_DOWN(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0) 

using namespace std;


void check(char c){//���1
	if(KEY_DOWN(c))
    {
        WinExec("DEMO_OFMOVE.exe 1",SW_HIDE);

        cout << c << " is down " << endl;
    }
}

void check_new(char c) {//���2
    if (KEY_DOWN(c))
    {
        WinExec("DEMO_OFMOVE.exe 2",SW_HIDE);

        cout << c << " is down " << endl;
    }
}

int main(){
	while(1){
		check('1');
        check_new('2');
		Sleep(20);//ѭ��ʱ��������ֹ̫ռ�ڴ� 
	}

	return 0;
}