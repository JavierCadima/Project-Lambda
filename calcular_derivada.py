import sympy
from sympy import symbols, sympify, diff, lambdify
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

def save_plot(figure, filename):
    """Oferece a opção de salvar o gráfico em PNG ou PDF na área de trabalho."""
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    file_path_png = os.path.join(desktop_path, f"{filename}.png")
    file_path_pdf = os.path.join(desktop_path, f"{filename}.pdf")
    
    try:
        figure.savefig(file_path_png, dpi=300)
        print(f"Gráfico salvo como '{file_path_png}' com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo PNG: {e}")

    try:
        figure.savefig(file_path_pdf)
        print(f"Gráfico salvo como '{file_path_pdf}' com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo PDF: {e}")

def calcular_derivada_1d():
    """Calcula a derivada de uma função de uma variável e opcionalmente plota o resultado."""
    try:
        func_str = input("Digite a função f(x): ")
        var_name = input("Digite a variável de diferenciação (ex: x): ")

        variavel = symbols(var_name)
        funcao = sympify(func_str)
        derivada = diff(funcao, variavel)

        print(f"\n--- Resultado ---")
        print(f"A derivada de {funcao} em relação a {variavel} é: {derivada}")
        
        plot_option = input("Deseja plotar o gráfico? (s/n): ").lower()
        if plot_option == 's':
            plot_1d_derivative(funcao, derivada, variavel)
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique se a função e a variável estão corretas. Detalhes do erro: {e}")

def plot_1d_derivative(funcao, derivada, variavel):
    """Plota a função original e sua derivada em um gráfico 2D."""
    try:
        func_numpy = lambdify(variavel, funcao, 'numpy')
        deriv_numpy = lambdify(variavel, derivada, 'numpy')

        x_vals = np.linspace(-10, 10, 400)
        y_vals = func_numpy(x_vals)
        y_deriv_vals = deriv_numpy(x_vals)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(x_vals, y_vals, label=f'f({variavel}) = {funcao}')
        ax.plot(x_vals, y_deriv_vals, label=f"f'({variavel}) = {derivada}", linestyle='--')
        
        ax.set_title(f"Gráfico de f({variavel}) e f'({variavel})")
        ax.set_xlabel(variavel)
        ax.set_ylabel("y")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True)
        ax.legend()

        filename = input("Digite o nome do arquivo para salvar (sem extensão): ")
        save_plot(fig, filename)
        
        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o gráfico: {e}")

def calcular_derivada_2d():
    """Calcula a derivada parcial de uma função de duas variáveis e opcionalmente plota o resultado."""
    try:
        func_str = input("Digite a função f(x, y): ")
        var_diff_str = input("Digite a variável para a qual você quer a derivada parcial (x ou y): ")
        
        x, y = symbols('x y')
        funcao = sympify(func_str)
        
        if var_diff_str == 'x':
            derivada = diff(funcao, x)
            print(f"\n--- Resultado ---")
            print(f"A derivada parcial de {funcao} em relação a x é: {derivada}")
        elif var_diff_str == 'y':
            derivada = diff(funcao, y)
            print(f"\n--- Resultado ---")
            print(f"A derivada parcial de {funcao} em relação a y é: {derivada}")
        else:
            print("Escolha inválida. Por favor, digite 'x' ou 'y'.")
            return
            
        plot_option = input("Deseja plotar o gráfico? (s/n): ").lower()
        if plot_option == 's':
            plot_3d_derivative(funcao, derivada, x, y)
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique se a função e a variável estão corretas. Detalhes do erro: {e}")

def plot_3d_derivative(funcao, derivada, x_sym, y_sym):
    """Plota a derivada parcial em um gráfico 3D."""
    try:
        func_numpy = lambdify((x_sym, y_sym), derivada, 'numpy')

        range_val = 3.0
        step = 0.1
        x_grid, y_grid = np.meshgrid(np.arange(-range_val, range_val + step, step),
                                     np.arange(-range_val, range_val + step, step))
        z_grid = func_numpy(x_grid, y_grid)

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none')
        ax.set_title(f'Gráfico da Derivada Parcial: z = {derivada}')
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_zlabel('Eixo Z')

        filename = input("Digite o nome do arquivo para salvar (sem extensão): ")
        save_plot(fig, filename)

        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o gráfico: {e}")

def calcular_derivada():
    """Menu principal para o cálculo de derivadas."""
    while True:
        print("\n--- Calculadora de Derivadas ---")
        print("Escolha o número de variáveis:")
        print("1. Uma variável (f(x))")
        print("2. Duas variáveis (f(x, y))")
        print("3. Voltar ao menu principal")
        
        choice = input("Sua escolha: ")
        
        if choice == '1':
            calcular_derivada_1d()
        elif choice == '2':
            calcular_derivada_2d()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    calcular_derivada()