pipeline {
  agent any
  stages {
    stage('git pull') {
      checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '061f33fc-b781-41a3-8f31-0cfca280b13d', url: 'https://github.com/tsbxmw/c-_show_config.git']]])
    }
    stage('build c files'){
      sh 'gcc -C -std=c99 date.c -o date.o'
    }
  }
}
