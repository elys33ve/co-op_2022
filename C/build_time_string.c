#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>      // #include <linux/ctype.h>


// will use __DATE__ and __TIME__ preprocessor directives but manipulate the strings to be yyyy:mm:dd:hh:mm:ss format
// should be a function that returns formated string


void format_date_time(char *date, char *time, char *str){
    char months[12][4] = {"jan\0","feb\0","mar\0","apr\0","may\0","jun\0","jul\0","aug\0","sep\0","oct\0","nov\0","dec\0"};
    char temp[4];
    int i;
    
    char year[5];
    char month[4];
    char day[3];

//      get date
    strncpy(year, date+7, 5);       // year

    strncpy(month, date, 3);        // month
    month[3] = 0;                       // end null char
    month[0] = tolower(month[0]);       // lowercase
    for (i=0;i<12;i++){
        strncpy(temp, months[i], 4);        // get from months list
        if (strcmp(temp, month) == 0){      // compare each
            if (i<9){                           // add first 0 if < 10
                sprintf(month, "0%d", i+1);
            }
            else {
                sprintf(month, "%d", i+1);
            }
            break;
        }
    }

    strncpy(day, date+4, 2);        // day
    day[2] = 0;                         // end null char
    if (isspace(day[0]) != 0){          // add first 0 if < 10
        day[0] = '0';
    }


///////////////////////// test
    printf("date: %s\n", date);
    printf("time: %s\n", time);
    printf("year: %s\n", year);
    printf("month: %s\n", month);
    printf("day: %s\n", day);


//      format
    strcpy(str, year); strcat(str, ":");
    strcat(str, month); strcat(str, ":");
    strcat(str, day); strcat(str, ":");
    strcat(str, time);
}


int main (){
    char *date = __DATE__;
    char *time = __TIME__;
    char build_time[20];

    format_date_time(date, time, build_time);

    printf("%s\n", build_time);

    return 0;
}
