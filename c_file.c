#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

void print_numbers(%d start_range, %d end_range) {

for (int i = start_range; i <= end_range; i++) {
printf("%d", i);
printf("%s", "\n");
}
}

int main (int argc, char *argv[]) {
    if (argc > 1) {
        if (strcmp(argv[1], "print_numbers") == 0) {
            print_numbers(atoi(argv[2]), atoi(argv[3]));
        }
    }
}