#include <stdio.h>
int main() {
    int num = 0;
    for(int _loop0 = 0; _loop0 < 5; _loop0++) {
    num = num + 1;
    if (num != 0) {
    printf("%d\n", num);
    } else {
    printf("%d\n", 0);
    }
    }
    return 0;
}
