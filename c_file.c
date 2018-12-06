#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

int* arr;
void insertion_sort(int* a) {
int start_loop = 1;
int end_loop = 5;

for (int i = start_loop; i <= end_loop; i++) {
int x = a[i];
int j = i;
while (j>1&&a[j-1]>x) {a[j] = a[j-1];
j = j-1;
}
a[j] = x;
}
}
void init_and_start(int e1, int e2, int e3, int e4, int e5) {
arr[1] = e1;
arr[2] = e2;
arr[3] = e3;
arr[4] = e4;
arr[5] = e5;
insertion_sort(arr);
printf("%d", arr[1]);
printf("%s", "\n");
printf("%d", arr[2]);
printf("%s", "\n");
printf("%d", arr[3]);
printf("%s", "\n");
printf("%d", arr[4]);
printf("%s", "\n");
printf("%d", arr[5]);
printf("%s", "\n");
}

int main (int argc, char *argv[]) {
arr = malloc ((5+1)*sizeof(int));
    if (argc > 1) {
        if (strcmp(argv[1], "init_and_start") == 0) {
            init_and_start(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]));
        }
    }
}