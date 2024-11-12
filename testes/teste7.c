#include <stdio.h>
int main() {
    int soma = 0;
    int multiplicador = 2;
    for(int _loop0 = 0; _loop0 < 3; _loop0++) {
    soma = soma + 5;
    multiplicador = multiplicador * 2;
    printf("%d\n", soma);
    printf("%d\n", multiplicador);
    }
    return 0;
}
