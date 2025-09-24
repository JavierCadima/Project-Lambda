import sympy
from sympy import symbols
from itertools import product

def main():
    """
    Calcula a tabela verdade de uma expressão booleana.
    """
    print("\n--- Calculadora de Tabela Verdade (Álgebra Booleana) ---")
    print("Use operadores: and, or, not, xor (ou ^), nand, nor, etc.")
    print("Exemplo: (A and B) or not C")
    print("---------------------------------------------------------")
    
    while True:
        try:
            expression_str = input("\nDigite a expressão booleana: ").lower()
            
            # Subistitui operadores lógicos por sintaxe do SymPy
            expression_str = expression_str.replace("and", "&")
            expression_str = expression_str.replace("or", "|")
            expression_str = expression_str.replace("not", "~")
            expression_str = expression_str.replace("xor", "^")

            # Encontra as variáveis na expressão
            vars_str = input("Digite as variáveis (separadas por vírgula, ex: A, B, C): ").replace(" ", "")
            variable_names = vars_str.split(',')
            
            if not variable_names or variable_names == ['']:
                print("Erro: Nenhuma variável foi fornecida.")
                continue

            # Cria os símbolos do SymPy para as variáveis
            variables = symbols(variable_names)
            
            # Converte a string da expressão em uma expressão simbólica
            expression = sympy.sympify(expression_str)
            
            # Cabeçalho da tabela
            header = variable_names + [expression_str]
            print("\n" + " | ".join(header))
            print("-" * (4 * len(header)))

            # Gera todas as combinações de valores booleanos para as variáveis
            num_vars = len(variable_names)
            for values in product([False, True], repeat=num_vars):
                # Cria um dicionário para substituir os símbolos por valores
                substitution_dict = dict(zip(variables, values))
                
                # Avalia a expressão para a combinação atual de valores
                result = expression.subs(substitution_dict)
                
                # Converte True/False para 1/0 para melhor visualização
                output_values = [int(v) for v in values]
                output_result = int(result)
                
                # Imprime a linha da tabela
                row = output_values + [output_result]
                print(" | ".join(map(str, row)))
            
        except (sympy.SympifyError, ValueError, TypeError) as e:
            print(f"\n--- Erro na Entrada! ---")
            print(f"Verifique se a expressão e as variáveis estão corretas.")
            print(f"Detalhes do erro: {e}")
            
        finally:
            continuar = input("\nDeseja calcular outra tabela verdade? (s/n, Enter para sim): ").lower()
            if continuar not in ['s', '']:
                break

if __name__ == '__main__':
    main()