#include "stdafx.h"

void LogShow::logwrite(string name, string logstr)
{
    string logname = name;
    FILE *fp;
    fp = fopen(logname.c_str(), "a");
    string endstr = "\n";
    logstr = logstr + endstr;
    fprintf(fp, logstr.c_str());
    fclose(fp);
}

void LogShow::logshow(string funcname, int loglevel, string logstr)
{
    cout << timeshow(funcname, loglevel) << logstr << endl;
}

std::string LogShow::timeshow()
{
    SYSTEMTIME sys;
    GetLocalTime(&sys);
    string timenow;
    if (sys.wMonth < 10)
        timenow = all2string.Word2String(sys.wYear) + ".0" + all2string.Word2String(sys.wMonth);
    else
        timenow = all2string.Word2String(sys.wYear) + "." + all2string.Word2String(sys.wMonth);
    if (sys.wDay < 10)
        timenow = timenow + ".0" + all2string.Word2String(sys.wDay) + " ";
    else
        timenow = timenow + "." + all2string.Word2String(sys.wDay) + " ";
    if (sys.wHour < 10)
        timenow += "0" + all2string.Word2String(sys.wHour) + ":";
    else
        timenow += all2string.Word2String(sys.wHour) + ":";
    if (sys.wMinute < 10)
        timenow += "0" + all2string.Word2String(sys.wMinute) + ":";
    else
        timenow += all2string.Word2String(sys.wMinute) + ":";
    if (sys.wSecond < 10)
        timenow += "0" + all2string.Word2String(sys.wSecond);
    else
        timenow += all2string.Word2String(sys.wSecond);


    return timenow;
}


std::string LogShow::timeshow(std::string showname)
{
    return timeshow() + " [ " + showname + " ]";
}

std::string LogShow::timeshow(std::string showname, std::string level)
{
    return timeshow(showname) + " (" + level + ") ";
}

std::string LogShow::timeshow(std::string showname, int level)
{
    /*
    Function::Log
    enum LogLevel {
    LogLevelError = 1,
    LogLevelWarning,
    LogLevelInfo,
    LogLevelDebug,
    LogLevelSystem,
    LogLevelNouse
    };
    */
    std::string loglevel = "Error";
    switch (level)
    {
    case 1:
        loglevel = "ERROR";
        break;
    case 2:
        loglevel = "WARNING";
        break;
    case 3:
        loglevel = "INFO";
        break;
    case 4:
        loglevel = "DEBUG";
        break;
    case 5:
        loglevel = "SYSTEM";
        break;
    case 6:
        loglevel = "????";
        break;
    default:
        loglevel = "INFO";
        break;
    }
    return timeshow(showname) + " (" + loglevel + ") ";
}