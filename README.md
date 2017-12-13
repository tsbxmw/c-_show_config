# Time Show on Ubuntu ( x86\x86_64\arm )

--------

## data_new 

* rewrite the function of show 
* get the time from the file
* use system() function to get the time  

## Build Statu

[![Build Status](https://travis-ci.org/tsbxmw/c-_show_config.svg?branch=master)](https://travis-ci.org/tsbxmw/c-_show_config)
[![Build status](https://ci.appveyor.com/api/projects/status/52bkbro1143l12dj?svg=true)](https://ci.appveyor.com/project/tsbxmw/c-show-config)


## details

> date.c
    
    the original version of date.c
    just show the TIME : xx:xx:xx 

> date_cubie.c

    the original version of date.c can run at arm-linux
    just modify some time get function and show function

## jenkins 

    in this dir ,some thing is like auto test struct here .
    called version 0.41 here , just include something of auto test .
    the code of autotest is defined at base/script , based on groovy ,can be running at jenkins .

    now also want to build a stable version 1.0 to using the auto test on a exe or jenkins or other website ...

    attention here : now all change to new project "python-auto-struct"
    (python-autotest-firmware)[https://github.com/tsbxmw/testshow/tree/master/python-autotest-firmware]

## something else

    try to build a new wall-paper to version2.0 , update the date_new.c to show more and more information .
    like android , using some setting to config it .
    


    