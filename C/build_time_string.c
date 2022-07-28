#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

// will use __DATE__ and __TIME__ preprocessor directives but manipulate the strings to be yyyy:mm:dd:hh:mm:ss format
// should be a function that returns formated string


void format_date_time(char *date, char *time, char *str){ 
    char months[12][4] = {"jan\0","feb\0","mar\0","apr\0","may\0","jun\0","jul\0","aug\0","sep\0","oct\0","nov\0","dec\0"};
    char temp[3];
    int i;
    
    char year[5];
    char month[4];
    char day[3];

//      get date
    strncpy(year, date+7, 5);       // year

    strncpy(month, date, 3);        // month
    month[3] = 0;
    month[0] = tolower(month[0]);
    for (i=0;i<12;i++){
        strncpy(temp, months[i], 4);
        if (strcmp(temp, month) == 0){
            if (i<9){
                sprintf(month, "0%d", i+1);
            }
            else {
                sprintf(month, "%d", i+1);
            }
            break;
        }
    }

    strncpy(day, date+4, 2);        // day
    day[2] = 0;

//      format
    strcpy(str, year); strcat(str, ":");
    strcat(str, month); strcat(str, ":");
    strcat(str, day); strcat(str, ":");
    strcat(str, time);
}


int main (){
    char *date = "Sep 01 9876";     // __DATE__
    char *time = "12:12:32";        // __TIME__
    char build_time[20];                  // char *build_time = kmalloc(20,GFP_KERNEL);   // for kernel

    format_date_time(date, time, build_time);

    printf("%s\n", build_time);

    return 0;
}
