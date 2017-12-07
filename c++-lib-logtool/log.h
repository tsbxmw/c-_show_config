#pragma once
#pragma once

#include <iostream>
#include "all2string.h"

using namespace std;



class LogShow {
public:

    All2String all2string;

    LogShow() { }
    ~LogShow() {}

    enum LogLevel {
        LogLevelError = 1,
        LogLevelWarning,
        LogLevelInfo,
        LogLevelDebug,
        LogLevelSystem,
        LogLevelNouse
    };

    enum LogWrite {
        LogWriteToFile = 10,
        LogWriteNo,
        LogWriteYes
    };

    // time show info
    //friend ostream& operator << (ostream & output, LogShow& tool);
    string timeshow();
    string timeshow(string showname);
    string timeshow(string showname, string level);
    string timeshow(string showname, int level);

    // log write
    void logwrite(string logname, string logstr);
    // log show
    void logshow(string funcname, int loglevel, string logstr);

};
