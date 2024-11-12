#include <stdio.h>
int main() {
    int a = 1;
    int b = 2;
    int c = 3;
    for(int _loop1 = 0; _loop1 < 2; _loop1++) {
    if (a != 0) {
    for(int _loop0 = 0; _loop0 < 2; _loop0++) {
    b = b + c;
    if (b != 0) {
    c = c * 2;
    } else {
    c = c + 1;
    }
    printf("%d\n", b);
    printf("%d\n", c);
    }
    } else {
    printf("%d\n", 0);
    }
    a = a + 1;
    }
    return 0;
}
