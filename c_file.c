#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
typedef struct {
} res_type;

typedef struct { i int; } routine_return_1
struct routine_return_1 a() {
int* result = malloc ((3+1)*sizeof(int));
res_type res;
return res;
}

int main (int argc, char *argv[]) {
    if (argc > 1) {
        if (strcmp(argv[1], "a") == 0) {
            a();
        }
    }
}