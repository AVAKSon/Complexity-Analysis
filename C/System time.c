
This probably isn't the best way to do this, but it works. 


It shows system time as "Www Mmm dd hh:mm:ss yyyy", where Www is the weekday, Mmm the month in letters, dd the day of the month, hh:mm:ss the time, and yyyy the year.
#include<time.h>
#include<stdio.h>
#include<stdlib.h>
int main(){
  time_t my_time = time(NULL);
  printf("%s", ctime(&my_time));
  return 0;
}
