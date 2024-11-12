#include <stdio.h>
int main() {
    int contador = 1;
    int soma = 0;
    int multiplicador = 2;
    for(int _loop0 = 0; _loop0 < 3; _loop0++) {
    if (contador != 0) {
    soma = soma + contador;
    multiplicador = multiplicador * 2;
    } else {
    soma = soma + 1;
    }
    printf("%d\n", soma);
    printf("%d\n", multiplicador);
    contador = contador + 1;
    }
    return 0;
}
