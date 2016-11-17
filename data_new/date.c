#include "my_date.h"

int main(){
while(1){
printf("\033[1;32m*****   **   ***   ***   *****    \n");
printf("\033[31m  *          *  * *  *   *           **\n");
printf("\033[1;34m  *     **   *   *   *   *****    \n");
printf("\033[1;33m  *     **   *   *   *   *           ** \n");
printf("\033[1;37m  *     **   *   *   *   *****    \n\n\n");

printf("\033\[1;37m\n");
FILE *stream;
char buf[50];
stream = popen("date","r");
fread(buf,sizeof(char),sizeof(buf),stream);
char *tmp;
int i = 0;
tmp = strtok(buf," ");
while(tmp!=NULL&&i<4){
    tmp = strtok(NULL," ");
    if(i==3){
        i = 4;
    }
    i++;
}
pclose(stream);
print_number(tmp);
//system("sleep 1");
usleep(100000);
system("clear");
}
return 0;
}

