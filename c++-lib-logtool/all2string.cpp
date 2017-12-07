#include "stdafx.h"


string All2String::Int2String(int value)
{
    stringstream ss;
    string str;
    ss << value;
    ss >> str;
    return str;
}

string All2String::Float2String(float value)
{
    stringstream ss;
    string str;
    ss << value;
    ss >> str;
    return str;
}

string All2String::Double2String(double value)
{
    stringstream ss;
    string str;
    ss << value;
    ss >> str;
    return str;
}

string All2String::Word2String(WORD w)
{
    char tmpbuff[16];
    sprintf(tmpbuff, "%d", w);
    string str = tmpbuff;
    return str;
}
