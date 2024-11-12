import os
import subprocess
import sys
from pathlib import Path

def run_single_test(test_path):
    """
    Executa um único arquivo de teste.
    Args:
        test_path: Path completo do arquivo de teste
    """
    try:
        # Converte o path para objeto Path para manipulação mais fácil
        test_path = Path(test_path)
        print(f"\n{'='*50}")
        print(f"Executando teste: {test_path.name}")
        print(f"{'='*50}")
        
        # Define os caminhos dos arquivos de saída no mesmo diretório do teste
        c_file = test_path.with_suffix('.c')
        exe_file = test_path.with_suffix('.exe')
        
        # Compila o arquivo .matemag para .c
        print("\nCompilando arquivo matemag...")
        result = subprocess.run(['python', 'main.py', str(test_path)], 
                              capture_output=True, 
                              text=True)
        
        # Verifica se o arquivo .c foi gerado
        if not c_file.exists():
            print(f"Erro: Arquivo {c_file} não foi gerado!")
            if result.stderr:
                print("Erro reportado:")
                print(result.stderr)
            return False
        
        print(f"Arquivo C gerado em: {c_file}")
            
        # Compila o arquivo .c gerado
        print("\nCompilando arquivo C...")
        result = subprocess.run(['gcc', str(c_file), '-o', str(exe_file)],
                              capture_output=True,
                              text=True)
                              
        if result.returncode != 0:
            print("Erro na compilação do arquivo C:")
            print(result.stderr)
            return False
        
        # Executa o programa
        print("\nExecutando o programa...")
        print("\nSaída do programa:")
        result = subprocess.run([str(exe_file)], capture_output=True, text=True)
        print(result.stdout)
        
        if result.stderr:
            print("\nErros durante a execução:")
            print(result.stderr)
            
        return True
        
    except Exception as e:
        print(f"\nErro ao executar teste: {str(e)}")
        return False
    finally:
        # Opcional: remover executável
        try:
            if exe_file.exists():
                exe_file.unlink()
        except:
            pass

def run_all_tests(tests_dir):
    """
    Executa todos os testes em um diretório.
    Args:
        tests_dir: Caminho para o diretório com os testes
    """
    # Converte para objeto Path
    tests_dir = Path(tests_dir)
    
    # Verifica se o diretório existe
    if not tests_dir.exists():
        print(f"Erro: Diretório {tests_dir} não encontrado!")
        return
    
    # Lista todos os arquivos .matemag no diretório
    test_files = list(tests_dir.glob('*.matemag'))
    
    if not test_files:
        print(f"Nenhum arquivo .matemag encontrado em {tests_dir}")
        return
    
    print(f"\nEncontrados {len(test_files)} arquivos de teste")
    
    # Contadores para o relatório
    total_tests = len(test_files)
    successful_tests = 0
    
    # Executa cada teste
    for test_file in test_files:
        if run_single_test(test_file):
            successful_tests += 1
    
    # Imprime relatório final
    print(f"\n{'='*50}")
    print("RELATÓRIO FINAL")
    print(f"{'='*50}")
    print(f"Total de testes: {total_tests}")
    print(f"Testes bem-sucedidos: {successful_tests}")
    print(f"Testes com falha: {total_tests - successful_tests}")
    print(f"Taxa de sucesso: {(successful_tests/total_tests)*100:.2f}%")
    
    # Lista os arquivos .c gerados
    print("\nArquivos .c gerados:")
    for test_file in test_files:
        c_file = test_file.with_suffix('.c')
        if c_file.exists():
            print(f"- {c_file}")

def main():
    # Se um diretório for especificado como argumento, usa ele
    # Caso contrário, assume que existe uma pasta 'testes' no diretório atual
    if len(sys.argv) > 1:
        tests_dir = sys.argv[1]
    else:
        tests_dir = 'testes'
    
    run_all_tests(tests_dir)

if __name__ == "__main__":
    main()