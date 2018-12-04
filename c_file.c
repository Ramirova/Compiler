#include <stdio.h>

int[3] my_array;
void bubble_sort() {
int start_loop = 1;
int end_loop = 3;
int start_second_loop = 1;
int end_second_loop = 3;
int flag = 1;
int temp = 0;
int one = 1;
int j = start_loop
for (int j = start_loop; j < end_loop; j++) {
int i = start_second_loop
for (int i = start_second_loop; i < (end_second_loop-j); i++) {
if (b[i]>b[i+1]) {
temp = b[i];b[i] = b[i+1];b[i+1] = temp;flag = 2;}
i = i+1;if (flag==1) {
i = 3;}
j = j+1;}
}
}
void init_and_start() {
int e1 = 1;
int e2 = 2;
int e3 = 3;
a[1] = e1;a[2] = e2;a[3] = e3;bubble_sort(a);}

int main (int argc, char *argv[]) {
if argc > 0 {
switch(argv[0]) {
case bubble_sort:
bubble_sort(argv)
break;
case init_and_start:
init_and_start(argv)
break;
default:
 break;
}
}