# README

## script of pipeline 

### dailybuild

    the Build-RPSG-RELEASE-Master pipeline

* build the other jobs 
* get the result of the build-jobs
* send the failed email to the fial-mail-to
* using to build daily build of master branch : edison and phoenix

### jenkins

    the ZEUS_AUTOTEST pipeline

* using to build the auto test struct
* include a lot of stage 
* send failed and success email

### jenkins_build

    the RUN_BUILD pipeline

* using to build the daily build job and auottest job
* according to the result , sending the report
