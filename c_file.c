#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

int partition(int* A, int lo, int hi) {
int pivot = A[hi];
int i = lo;
int j = 0;

for (int j = lo; j <= (hi-1); j++) {
if (A[j]<=pivot) {
int temp = A[j];
A[j] = A[i];
A[i] = A[j];
i = i+1;
}
}
int temp = A[i];
A[j] = A[hi];
A[hi] = A[i];
return i;
}
int*  quicksort(int* A, int lo, int hi) {
if (lo<hi) {
int p;
p = (int)partition(A,lo,hi);
quicksort(A,lo,(p-1));
quicksort(A,(p+1),hi);
}
return A;
}
void init_and_start(int e1, int e2, int e3, int e4, int e5) {
int* a = malloc ((5+1)*sizeof(int));
a[1] = e1;
a[2] = e2;
a[3] = e3;
a[4] = e4;
a[5] = e5;
quicksort(a,1,5);
printf("%d", a[1]);
printf("%s", "\n");
printf("%d", a[2]);
printf("%s", "\n");
printf("%d", a[3]);
printf("%s", "\n");
printf("%d", a[4]);
printf("%s", "\n");
printf("%d", a[5]);
printf("%s", "\n");
}

int main (int argc, char *argv[]) {
    if (argc > 1) {
        if (strcmp(argv[1], "init_and_start") == 0) {
            init_and_start(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]));
        }
    }
}