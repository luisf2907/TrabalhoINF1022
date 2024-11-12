import ply.lex as lex
import ply.yacc as yacc
import sys

# Lista dos tokens
tokens = (
    'FACA', 'SER', 'MOSTRE', 'SOME', 'COM', 'REPITA', 'VEZES', 'SE', 'ENTAO', 
    'SENAO', 'MULTIPLIQUE', 'POR', 'ID', 'NUMBER', 'DOT', 'COLON', 'FIM'
)

# Regras de expressões regulares para tokens simples
t_DOT = r'\.'
t_COLON = r':'
t_ignore = ' \t'

# Tokens de palavras-chave reservadas
reserved = {
    'FACA': 'FACA',
    'SER': 'SER',
    'MOSTRE': 'MOSTRE',
    'SOME': 'SOME',
    'COM': 'COM',
    'REPITA': 'REPITA',
    'VEZES': 'VEZES',
    'SE': 'SE',
    'ENTAO': 'ENTAO',
    'SENAO': 'SENAO',
    'MULTIPLIQUE': 'MULTIPLIQUE',
    'POR': 'POR',
    'FIM': 'FIM'
}

# Variáveis globais
resultado_operacao_usado = False
loop_counter = 0

def reset_compiler_state():
    global resultado_operacao_usado, loop_counter
    resultado_operacao_usado = False
    loop_counter = 0

# Tokens para identificadores e números
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'  # Permite letras seguidas de letras ou números
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere não permitido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Definir a gramática e as funções de manipulação
def p_programa(p):
    'programa : cmds'
    global resultado_operacao_usado
    
    if p[1] is None or p[1].strip() == "":
        p[0] = "#include <stdio.h>\nint main() {\n    return 0;\n}\n"
        return
        
    codigo = "#include <stdio.h>\nint main() {\n"
    if resultado_operacao_usado:
        codigo += "    int resultado_operacao;\n"
    codigo += p[1]
    codigo += "    return 0;\n}\n"
    
    p[0] = codigo

def p_cmds_multiple(p):
    'cmds : cmd cmds'
    p[0] = p[1] + p[2]

def p_cmds_single(p):
    'cmds : cmd'
    p[0] = p[1]

def p_cmd_atribuicao(p):
    'cmd : FACA ID SER NUMBER DOT'
    p[0] = f"    int {p[2]} = {p[4]};\n"

def p_cmd_impressao_var(p):
    'cmd : MOSTRE ID DOT'
    p[0] = f'    printf("%d\\n", {p[2]});\n'

def p_cmd_impressao_num(p):
    'cmd : MOSTRE NUMBER DOT'
    p[0] = f'    printf("%d\\n", {p[2]});\n'

# Regras para MOSTRE operacao
def p_cmd_impressao_operacao_soma(p):
    'cmd : MOSTRE SOME ID COM ID DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} + {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_soma_num(p):
    'cmd : MOSTRE SOME ID COM NUMBER DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} + {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_soma_num_id(p):
    'cmd : MOSTRE SOME NUMBER COM ID DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} + {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_soma_nums(p):
    'cmd : MOSTRE SOME NUMBER COM NUMBER DOT'
    resultado = p[3] + p[5]
    p[0] = f"    printf(\"%d\\n\", {resultado});\n"

def p_cmd_impressao_operacao_mult(p):
    'cmd : MOSTRE MULTIPLIQUE ID POR ID DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} * {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_mult_num(p):
    'cmd : MOSTRE MULTIPLIQUE ID POR NUMBER DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} * {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_mult_num_id(p):
    'cmd : MOSTRE MULTIPLIQUE NUMBER POR ID DOT'
    global resultado_operacao_usado
    resultado_operacao_usado = True
    p[0] = f"    resultado_operacao = {p[3]} * {p[5]};\n    printf(\"%d\\n\", resultado_operacao);\n"

def p_cmd_impressao_operacao_mult_nums(p):
    'cmd : MOSTRE MULTIPLIQUE NUMBER POR NUMBER DOT'
    resultado = p[3] * p[5]
    p[0] = f"    printf(\"%d\\n\", {resultado});\n"

# Regras para operações normais
def p_cmd_soma_var_var(p):
    'cmd : SOME ID COM ID DOT'
    p[0] = f"    {p[2]} = {p[2]} + {p[4]};\n"

def p_cmd_soma_var_num(p):
    'cmd : SOME ID COM NUMBER DOT'
    p[0] = f"    {p[2]} = {p[2]} + {p[4]};\n"

def p_cmd_soma_num_num(p):
    'cmd : SOME NUMBER COM NUMBER DOT'
    resultado = p[2] + p[4]
    p[0] = f"    printf(\"%d\\n\", {resultado});\n"

def p_cmd_multiplicacao_var_var(p):
    'cmd : MULTIPLIQUE ID POR ID DOT'
    p[0] = f"    {p[2]} = {p[2]} * {p[4]};\n"

def p_cmd_multiplicacao_var_num(p):
    'cmd : MULTIPLIQUE ID POR NUMBER DOT'
    p[0] = f"    {p[2]} = {p[2]} * {p[4]};\n"

def p_cmd_multiplicacao_num_num(p):
    'cmd : MULTIPLIQUE NUMBER POR NUMBER DOT'
    resultado = p[2] * p[4]
    p[0] = f"    printf(\"%d\\n\", {resultado});\n"

def p_cmd_repeticao(p):
    'cmd : REPITA NUMBER VEZES COLON cmds FIM'
    global loop_counter
    current_loop = f"_loop{loop_counter}"
    loop_counter += 1
    p[0] = f"    for(int {current_loop} = 0; {current_loop} < {p[2]}; {current_loop}++) {{\n{p[5]}    }}\n"

def p_cmd_condicional_se_entao(p):
    'cmd : SE ID ENTAO cmds FIM'
    p[0] = f"    if ({p[2]} != 0) {{\n{p[4]}    }}\n"

def p_cmd_condicional_se_entao_senao(p):
    'cmd : SE ID ENTAO cmds SENAO cmds FIM'
    p[0] = f"    if ({p[2]} != 0) {{\n{p[4]}    }} else {{\n{p[6]}    }}\n"

def p_cmd_condicional_se_num_entao(p):
    'cmd : SE NUMBER ENTAO cmds FIM'
    p[0] = f"    if ({p[2]} != 0) {{\n{p[4]}    }}\n"

def p_cmd_condicional_se_num_entao_senao(p):
    'cmd : SE NUMBER ENTAO cmds SENAO cmds FIM'
    p[0] = f"    if ({p[2]} != 0) {{\n{p[4]}    }} else {{\n{p[6]}    }}\n"

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo")

# Construir o parser
parser = yacc.yacc()

def compile_matemagica(input_file):
    """Compila um arquivo Matemágica para C."""
    reset_compiler_state()
    
    try:
        if not input_file.endswith('.matemag'):
            raise ValueError("O arquivo deve ter a extensão .matemag")
        
        with open(input_file, 'r') as f:
            data = f.read()
        
        # Tenta fazer o parse do código
        result = parser.parse(data)
        if result is None or result == "":
            raise Exception("Erro na compilação")
            
        # Gera o arquivo de saída
        output_file = input_file[:-8] + '.c'
        with open(output_file, 'w') as f:
            f.write(result)
            
        print(f"Arquivo '{output_file}' gerado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro durante a compilação: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        input_file = input("Digite o nome do arquivo de entrada (.matemag): ")
    else:
        input_file = sys.argv[1]
    
    compile_matemagica(input_file)

if __name__ == "__main__":
    main()