
#include<sys/types.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<stdio.h>
void strcpy_1(char a[8][6],char b[8][6]){
    for(int i =0;i<8;i++)
            for(int j=0;j<6;j++)
                    a[i][j] = b[i][j];

}

void print_number(char *date){
        char a0[8][6] = {" *** ",
                         "*   *",
                         "*   *",
                         "*   *",
                         "*   *",
                         "*   *",
                         "*   *",
                         " *** "};
        char a1[8][6] = {"  *  ",
                         " **  ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "*****"};
        char a2[8][6] = {" *** ",
                         "*   *",
                         "*   *",
                         "   * ",
                         "  *  ",
                         " *   ",
                         "*   *",
                         "*****"};
        char a3[8][6] = {" *** ",
                         "*   *",
                         "    *",
                         "  ** ",
                         "    *",
                         "    *",
                         "*   *",
                         " *** "};
        char a4[8][6] = {"   * ",
                         "  ** ",
                         " * * ",
                         "*  * ",
                         "*  * ",
                         " ****",
                         "   * ",
                         "  ***"};
        char a5[8][6] = {"*****",
                         "*    ",
                         "*    ",
                         "**** ",
                         "    *",
                         "    *",
                         "*   *",
                         " *** "};
        char a6[8][6] = {" *** ",
                         "*   *",
                         "*    ",
                         "**** ",
                         "*   *",
                         "*   *",
                         "*   *",
                         " *** "};
        char a7[8][6] = {"*****",
                         "*   *",
                         "   * ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "  *  "};
        char a8[8][6] = {" *** ",
                         "*   *",
                         "*   *",
                         " *** ",
                         "*   *",
                         "*   *",
                         "*   *",
                         " *** "};
        char a9[8][6] = {" *** ",
                         "*   *",
                         "*   *",
                         "*   *",
                         " ****",
                         "    *",
                         "*   *",
                         " *** "};
        char ax[8][6] = {"     ",
                         "  ** ",
                         "  ** ",
                         "     ",
                         "     ",
                         "  ** ",
                         "  ** ",
                         "     "};
        char ad_Y[8][6] = {
                         "     ",
                         "*   *",
                         "*   *",
                         " * * ",
                         "  *  ",
                         "  *  ",
                         "  *  ",
                         "     "}；
        char ad_M[8][6] = {
                         "     ",
                         "*   *",
                         "** **",
                         "* * *",
                         "* * *",
                         "* * *",
                         "*   *",
                         "     "};
        char ad_D[8][6] = {
                         "     ",
                         "**** ",
                         "*   *",
                         "*   *",
                         "*   *",
                         "*   *",
                         "**** ",
                         "     "};
         char xspace[8][3]={"  ","  ","  ","  ","  ","  ","  ","  "};

        char temp;
        char time_temp[8][6];
        int i = 0;
        char time[8][200];
        for(int i=0;i<8;i++)
                for(int j=0;j<200;j++)
                        time[i][j]='\0';
        while((temp=date[i])!=NULL){
            if(temp =='1')
                    strcpy_1(time_temp,a1);
            if(temp =='2')
                    strcpy_1(time_temp,a2);
            if(temp =='3')
                    strcpy_1(time_temp,a3);
            if(temp =='4')
                    strcpy_1(time_temp,a4);
            if(temp =='5')
                    strcpy_1(time_temp,a5);
            if(temp =='6')
                    strcpy_1(time_temp,a6);
            if(temp =='7')
                    strcpy_1(time_temp,a7);
            if(temp =='8')
                    strcpy_1(time_temp,a8);
            if(temp =='9')
                    strcpy_1(time_temp,a9);
            if(temp =='0')
                    strcpy_1(time_temp,a0);
            if(temp ==':')
                    strcpy_1(time_temp,ax);
            for(int j=0;j<8;j++){
                int m = i*8;

                int n = (i+1)*8;
                time[j][m] = xspace[j][0];
                m++;
                time[j][m] = xspace[j][1];
                m++;
                for(int x=0;m<n;m++){
                        time[j][m]=time_temp[j][x];
                        x++;
                }
               // if(i==0)
                 //   for(int x=0;x<n;x++)
                   //     printf("%c",time[j][x]);
                //time_x = strcat(time[j],xspace[j]);
                //time[j] = strcat(time_x[j],time_temp);
            }
            i++;
        }

        for(int i=0;i<8;i++)
        {



               for(int j=0;j<200;j++)
               {
                    int x = rand()%7;

                    if(time[i][j]!='\0')
                    {
                        if(x%6==0)
                            printf("\033[1;32m%c",time[i][j]);
                        if(x%6==1)
                            printf("\033[1;33m%c",time[i][j]);
                        if(x%6==2)
                            printf("\033[1;34m%c",time[i][j]);
                        if(x%6==3)
                            printf("\033[1;35m%c",time[i][j]);
                        if(x%6==4)
                            printf("\033[1;36m%c",time[i][j]);
                        if(x%6==5)
                            printf("\033[1;37m%c",time[i][j]);
                    }
               }
               printf("\n");
        }
}
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
memset(buf,'\0',sizeof(buf));
stream = popen("date","r");
fread(buf,sizeof(char),sizeof(buf),stream);
pclose(stream);
char *tmp;
system("date > hello");
stream = fopen("hello","r");
fgets(buf,50,stream);
fclose(stream);
int i = 0;
tmp = strtok(buf," ");
while(tmp!=NULL&&i<4){
    tmp = strtok(NULL," ");
    if(i==2){
        i = 4;
    }
    i++;
}
//pclose(stream);
print_number(tmp);
usleep(80000);
system("clear");
}
return 0;
}
