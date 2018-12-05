#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
typedef struct {
int i
;
} my_rec_type;
typedef my_arr my_arr[(3+1)];

my_rec_type my_rec = {0};
*my_arr a(int rec) {
int* result = malloc ((3+1)*sizeof(int));
return result;
}
my_rec input;
my_arr in_arr;
int* result = a(1);

int main (int argc, char *argv[]) {
result = malloc (*sizeof(int));
    if (argc > 1) {
        if (strcmp(argv[1], "a") == 0) {
            a(atoi(argv[2]));
        }
    }
}