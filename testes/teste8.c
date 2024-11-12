#include <stdio.h>
int main() {
    int x = 1;
    for(int _loop1 = 0; _loop1 < 3; _loop1++) {
    for(int _loop0 = 0; _loop0 < 2; _loop0++) {
    x = x + 1;
    printf("%d\n", x);
    }
    }
    return 0;
}
