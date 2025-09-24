import sympy
from sympy import symbols, sympify

def main():
    """
    Calculadora de valor de função para N variáveis usando a biblioteca SymPy.
    """
    print("--- Calculadora de Valor de Função (Múltiplas Variáveis) ---")
    print("Exemplo: Para f(x, y) = x**2 + y**2, e x=2, y=3, digite:")
    print("Variáveis: x, y")
    print("Valores: 2, 3")
    print("-----------------------------------------------------------")

    while True:
        try:
            # Pede a função, as variáveis e os valores
            func_str = input("\nDigite a função (ex: x**2 + y**2 + z): ")
            vars_str = input("Digite as variáveis separadas por vírgula (ex: x, y, z): ")
            vals_str = input("Digite os valores correspondentes separados por vírgula (ex: 1, 2, 3): ")
            
            # Converte as strings de entrada em listas de strings
            var_names = [v.strip() for v in vars_str.split(',')]
            val_strs = [v.strip() for v in vals_str.split(',')]
            
            # Verifica se o número de variáveis e valores corresponde
            if len(var_names) != len(val_strs):
                raise ValueError("O número de variáveis e valores não corresponde. Por favor, tente novamente.")
                
            # Cria os símbolos e os valores para a substituição
            variaveis = symbols(' '.join(var_names))
            valores = [sympify(v) for v in val_strs]
            
            # Cria um dicionário de substituição
            substituicoes = dict(zip(variaveis, valores))
            
            # Converte a string da função em uma expressão simbólica
            funcao = sympify(func_str)
            
            # Realiza a substituição e calcula o resultado
            resultado = funcao.subs(substituicoes)

            print(f"\n--- Resultado ---")
            print(f"Para a função {funcao} com as substituições {substituicoes}, o valor é: {resultado}")

        except (sympy.SympifyError, ValueError, TypeError, IndexError) as e:
            print(f"\n--- Erro! ---")
            print(f"Entrada inválida. Verifique a sintaxe ou o número de variáveis e valores.")
            print(f"Detalhes do erro: {e}")
        
        continuar = input("\n\nDeseja calcular outro valor? (s/n): ").lower()
        if continuar != 's':
            break

def calular_valor_funcao_n_variaveis():
    main()