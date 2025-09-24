import json
import os
import plotar_grafico
import plotar_grafico_3d
import plotar_grafico_2d
import plotar_curvas_de_nivel
import newton_raphson
import calcular_limite
import calcular_derivada
import calcular_integral
import calcular_extremos
import calcular_valor_funcao_n_variaveis

SUBSTITUTIONS_FILE = 'substitutions.json'

def view_functions():
    """Visualiza as funções e comandos personalizados."""
    try:
        with open(SUBSTITUTIONS_FILE, 'r') as f:
            substitutions = json.load(f)
            print("\n--- Funções e Comandos Suportados ---")
            for key, value in substitutions.items():
                print(f"  - {key} (substituído por: {value})")
            print("--------------------------------------")
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNenhuma função personalizada encontrada. Usando substituições padrão.")

def add_function():
    """Adiciona uma nova função/comando ao arquivo de substituições."""
    print("\n--- Adicionar Nova Função ---")
    new_func = input("Digite a função a ser substituída (ex: 'logb'): ")
    lua_syntax = input("Digite a sintaxe Lua correspondente (ex: 'math.log(b)'): ")

    try:
        substitutions = {}
        if os.path.exists(SUBSTITUTIONS_FILE):
            with open(SUBSTITUTIONS_FILE, 'r') as f:
                substitutions = json.load(f)

        substitutions[new_func] = lua_syntax

        with open(SUBSTITUTIONS_FILE, 'w') as f:
            json.dump(substitutions, f, indent=4)
        
        print("\nFunção adicionada com sucesso!")
        
    except Exception as e:
        print(f"\nErro ao adicionar a função: {e}")

def main():
    """Menu principal da calculadora de equações e gráficos."""
    while True:
        print("\n" + "=" * 30)
        print("    Calculadora de Gráficos e Funções")
        print("=" * 30)
        print("Opções:")
        print("1. Plotar Superfície de Nível (z = f(x, y, z))")
        print("2. Plotar Gráfico 3D de Função (z = f(x, y))")
        print("3. Plotar Gráfico 2D de Função (y = f(x))")
        print("4. Plotar Curvas de Nível (z = f(x, y))")
        print("5. Encontrar Raiz (Método de Newton-Raphson)")
        print("6. Calcular Limites")
        print("7. Calcular Derivadas")
        print("8. Calcular Integrais")
        print("9. Encontrar Máximos e Mínimos")
        print("10. Calcular Valor da Função (N variáveis)")
        print("11. Gerenciar Funções (Adicionar/Ver)")
        print("12. Sair")
        print("-" * 30)
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            plotar_grafico.plot_superficiedenivel()
        elif choice == '2':
            plotar_grafico_3d.plot_function3d()
        elif choice == '3':
            plotar_grafico_2d.plotar_grafico_2d()
        elif choice == '4':
            plotar_curvas_de_nivel.plot_curves_of_level()
        elif choice == '5':
            newton_raphson.newton_raphson_calculator()
        elif choice == '6':
            calcular_limite.limite_calculator()
        elif choice == '7':
            calcular_derivada.calcular_derivada()
        elif choice == '8':
            calcular_integral.calcular_integral()
        elif choice == '9':
            # Linha corrigida
            calcular_extremos.main()
        elif choice == '10':
            calcular_valor_funcao_n_variaveis.calular_valor_funcao_n_variaveis()
        elif choice == '11':
            sub_choice = input("Ver Funções (v) ou Adicionar Funções (a)?: ").lower()
            if sub_choice == 'v':
                view_functions()
            elif sub_choice == 'a':
                add_function()
            else:
                print("Opção inválida.")
        elif choice == '12':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    main()