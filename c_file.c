#include <stdio.h>

void init_and_start() {
int e1 = 1;
return e1;
}
int[3] my_array;
int res = init_and_start(my_array);

int main (int argc, char *argv[]) {
if argc > 0 {
switch(argv[0]) {
case init_and_start:
init_and_start(argv)
break;
default:
 break;
}
}