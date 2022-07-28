#include <stdio.h>
#include <ctype.h>
#include <string.h>

// will use __DATE__ and __TIME__ preprocessor directives but manipulate the strings to be yyyy:mm:dd:hh:mm:ss format

int main (){
    char months[12][4] = {"jan\0","feb\0","mar\0","apr\0","may\0","jun\0","jul\0","aug\0","sep\0","oct\0","nov\0","dec\0"};

    char *date = "Jul 16 2022\0";
    char *time = "20:12:42";
    char str[20];

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

    
    printf("date: %s\n", date);
    printf("time: %s\n", time);
    printf("year: %s\n", year);
    printf("month: %s\n", month);
    printf("day: %s\n", day);

//      format and print
    strcpy(str, year); str[4] = ':';
    strcat(str, month); str[8] = ':';
    strcat(str, day); str[11] = ':';
    strcat(str, time);

    printf("%s\n", str);

    return 0;
}
