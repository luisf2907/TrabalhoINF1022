# Relatório Final: Compilador da Linguagem Matemágica
**Disciplina**: INF1022 - 2024.2  
**Professores**: Vitor Pinheiro e Edward Hermann
**Alunos**: Luís Felipe Werneck (2111044) e David Wolff (2012428)

## 1. Introdução

Este trabalho implementa um compilador para a linguagem Matemágica, convertendo código Matemágica em código C. O compilador foi desenvolvido utilizando Python com as bibliotecas PLY (Python Lex-Yacc) que implementa o método LALR(1).

## 2. Gramática

### 2.1 Gramática Original (do PDF)
```
programa → cmds
cmds → cmd cmds | cmd
cmd → atribuicao | impressao | operacao | repeticao
atribuicao → FACA var SER num.
impressao → MOSTRE var. | MOSTRE operacao.
operacao → SOME var COM var. | SOME var COM num. | SOME num COM num.
repeticao → REPITA num VEZES : cmds FIM
```

### 2.2 Gramática Modificada
```
programa → cmds
cmds → cmd cmds | cmd
cmd → atribuicao | impressao | operacao | repeticao | condicional
atribuicao → FACA var SER num DOT
impressao → MOSTRE var DOT | MOSTRE num DOT | MOSTRE operacao DOT
operacao → soma | multiplicacao
soma → SOME var COM var DOT | SOME var COM num DOT | SOME num COM num DOT
multiplicacao → MULTIPLIQUE var POR var DOT | MULTIPLIQUE var POR num DOT | MULTIPLIQUE num POR num DOT
repeticao → REPITA num VEZES COLON cmds FIM
condicional → SE var ENTAO cmds FIM | SE var ENTAO cmds SENAO cmds FIM | SE num ENTAO cmds FIM | SE num ENTAO cmds SENAO cmds FIM
```

### 2.3 Modificações da Gramática

1. **Adição de Multiplicação**:
   - Incluídas regras para multiplicação entre variáveis e números
   - Formatos: `MULTIPLIQUE var POR var` e `MULTIPLIQUE var POR num`

2. **Adição de Condicionais**:
   - Implementados comandos SE-ENTAO e SE-ENTAO-SENAO
   - Incluído suporte para condicionais com números diretos além de variáveis

3. **Extensão de Operações**:
   - Adicionado suporte para operações diretas entre números
   - Incluída impressão do resultado de operações

## 3. Implementação

### 3.1 Análise Léxica

Os tokens definidos para a linguagem:
```python
tokens = (
    'FACA', 'SER', 'MOSTRE', 'SOME', 'COM', 'REPITA', 'VEZES', 'SE', 'ENTAO', 
    'SENAO', 'MULTIPLIQUE', 'POR', 'ID', 'NUMBER', 'DOT', 'COLON', 'FIM'
)
```

Expressões regulares para tokens especiais:
```python
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'  # Permite letras seguidas de letras ou números
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'  # Números: apenas inteiros não-negativos
    t.value = int(t.value)
    return t
```

### 3.2 Análise Sintática

O analisador sintático foi implementado usando regras de produção que geram código C equivalente. Exemplo de regras:

```python
def p_cmd_impressao_operacao_soma(p):
    'cmd : MOSTRE SOME ID COM ID DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} + {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_multiplicacao_var_var(p):
    'cmd : MULTIPLIQUE ID POR ID DOT'
    p[0] = f"    {p[2]} = {p[2]} * {p[4]};\n"
```

## 4. Casos de Teste

### 4.1 Teste de Atribuições Básicas
```
FACA a SER 10.
FACA b SER 5.
FACA resultado SER 0.
MOSTRE a.
MOSTRE b.
MOSTRE resultado.
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int a = 10;
    int b = 5;
    int resultado = 0;
    printf("%d\n", a);
    printf("%d\n", b);
    printf("%d\n", resultado);
    return 0;
}
```

### 4.2 Teste de Operações de Soma
```
FACA x SER 5.
FACA y SER 3.
SOME x COM y.
MOSTRE x.
SOME x COM 10.
MOSTRE x.
SOME 20 COM 30.
MOSTRE x.
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int x = 5;
    int y = 3;
    x = x + y;
    printf("%d\n", x);
    x = x + 10;
    printf("%d\n", x);
    printf("%d\n", 50);
    printf("%d\n", x);
    return 0;
}
```

### 4.3 Teste de MOSTRE operacao
```
FACA x SER 5.
FACA y SER 3.
MOSTRE SOME x COM y.
FACA a SER 4.
FACA b SER 2.
MOSTRE MULTIPLIQUE a POR b.
MOSTRE SOME 10 COM 20.
MOSTRE MULTIPLIQUE 5 POR 3.
MOSTRE SOME x COM 10.
MOSTRE MULTIPLIQUE a POR 3.
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int resultado_operacao;
    int x = 5;
    int y = 3;
    resultado_operacao = x + y;
    printf("%d\n", resultado_operacao);
    int a = 4;
    int b = 2;
    resultado_operacao = a * b;
    printf("%d\n", resultado_operacao);
    printf("%d\n", 30);
    printf("%d\n", 15);
    resultado_operacao = x + 10;
    printf("%d\n", resultado_operacao);
    resultado_operacao = a * 3;
    printf("%d\n", resultado_operacao);
    return 0;
}
```

### 4.4 Teste de Condicionais SE-ENTAO
```
FACA valor SER 1.
SE valor ENTAO
    MOSTRE valor.
FIM
FACA zero SER 0.
SE zero ENTAO
    MOSTRE zero.
FIM
SE 1 ENTAO
    MOSTRE 100.
FIM
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int valor = 1;
    if (valor != 0) {
        printf("%d\n", valor);
    }
    int zero = 0;
    if (zero != 0) {
        printf("%d\n", zero);
    }
    if (1 != 0) {
        printf("%d\n", 100);
    }
    return 0;
}
```

### 4.5 Teste de Condicionais SE-ENTAO-SENAO
```
FACA numero SER 1.
SE numero ENTAO
    MOSTRE 10.
SENAO
    MOSTRE 20.
FIM
FACA zero SER 0.
SE zero ENTAO
    MOSTRE 30.
SENAO
    MOSTRE 40.
FIM
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int numero = 1;
    if (numero != 0) {
        printf("%d\n", 10);
    } else {
        printf("%d\n", 20);
    }
    int zero = 0;
    if (zero != 0) {
        printf("%d\n", 30);
    } else {
        printf("%d\n", 40);
    }
    return 0;
}
```

### 4.6 Teste de Repetição
```
FACA contador SER 0.
REPITA 5 VEZES:
    SOME contador COM 1.
    MOSTRE contador.
FIM
```
Saída C gerada:
```c
#include <stdio.h>
int main() {
    int contador = 0;
    for(int _loop0 = 0; _loop0 < 5; _loop0++) {
        contador = contador + 1;
        printf("%d\n", contador);
    }
    return 0;
}
```

### 4.7 Teste Complexo (Combinação de Estruturas)
```
FACA a SER 1.
FACA b SER 2.
FACA c SER 3.
REPITA 2 VEZES:
    SE a ENTAO
        REPITA 2 VEZES:
            SOME b COM c.
            SE b ENTAO
                MULTIPLIQUE c POR 2.
            SENAO
                SOME c COM 1.
            FIM
            MOSTRE b.
            MOSTRE c.
        FIM
    SENAO
        MOSTRE 0.
    FIM
    SOME a COM 1.
FIM
```

## 5. Funcionalidades Implementadas

- ✓ Atribuição de valores
- ✓ Operações de soma (var-var, var-num, num-num)
- ✓ Operações de multiplicação (var-var, var-num, num-num)
- ✓ Estruturas de repetição
- ✓ Condicionais SE-ENTAO com avaliação numérica
- ✓ Condicionais SE-ENTAO-SENAO
- ✓ MOSTRE operacao
- ✓ Operações com números diretos
- ✓ Estruturas aninhadas
- ✓ Identificadores com números (ex: num1, var2)

## 6. Como Executar

### 6.1 Requisitos
- Python 3.x
- PLY (Python Lex-Yacc)
- GCC (para compilar o código C gerado)

### 6.2 Instalação
```bash
pip install ply
```

### 6.3 Compilação
```bash
python compilador_matematica.py programa.matemag
```

### 6.4 Execução dos Testes
```bash
python run_tests.py pasta_testes
```

## 7. Conclusão

O compilador implementa todas as funcionalidades requeridas da linguagem Matemágica, incluindo as extensões solicitadas (SE-ENTAO-SENAO, multiplicação e MOSTRE operacao). A implementação foi validada através de um conjunto abrangente de testes que cobrem todos os aspectos da linguagem, incluindo casos básicos e complexos com estruturas aninhadas.