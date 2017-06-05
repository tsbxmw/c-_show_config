# Time Show on Ubuntu ( x86\x86_64\arm )

--------

## data_new 

* rewrite the function of show 
* get the time from the file
* use system() function to get the time  

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

    