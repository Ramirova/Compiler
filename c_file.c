#include <stdio.h>
#include <stdbool.h>
#include <string.h>
typedef int sorting_array_type[3];
sorting_array_type my_array;
void bubble_sort(sorting_array_type b) {
int start_loop = 1;
int end_loop = 3;
int start_second_loop = 1;
int end_second_loop = 3;
int flag = 1;
int temp = 0;

for (int j = start_loop; j < end_loop; j++) {

for (int i = start_second_loop; i < (end_second_loop-j); i++) {
if (b[i]>b[i+1]) {
temp = b[i];b[i] = b[i+1];b[i+1] = temp;flag = 2;}
i = i+1;if (flag==1) {
i = 3;}
j = j+1;}
}
}
void init_and_start(int param) {
int e1 = 3;
int e2 = 2;
int e3 = 1;
int a[3];
a[0] = e1;a[1] = e2;a[2] = e3;bubble_sort(a);}
void insertion_sort(sorting_array_type a) {
int start_loop = 2;
int end_loop = 3;

for (int i = start_loop; i < end_loop; i++) {
int x = a[i];
int j = i;
while (j>1&&a[j-1]>x) {a[j] = a[j-1];j = j-1;}
a[j] = x;}
}

int main (int argc, char *argv[]) {
if (argc > 1) {
if (strcmp(argv[1], "init_and_start") > 0) {
init_and_start((int) argv[2]);
}

}
}