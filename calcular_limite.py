import sympy
from sympy import symbols, limit, sympify, lambdify
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

def calcular_limite_1d():
    """Calcula limites de uma função de uma variável e opcionalmente plota a função."""
    try:
        func_str = input("Digite a função (ex: sin(x)/x): ")
        ponto_str = input("Digite o ponto do limite (ex: 0): ")
        direcao = input("Direção do limite (+ para direita, - para esquerda, Enter para bilateral): ")

        x = symbols('x')
        funcao = sympify(func_str)
        ponto = sympify(ponto_str)

        dir_arg = '+' if direcao == '+' else '-' if direcao == '-' else 'real'
        if dir_arg == 'real':
            resultado = limit(funcao, x, ponto)
        else:
            resultado = limit(funcao, x, ponto, dir=dir_arg)

        tipo_limite = "bilateral" if dir_arg == 'real' else "superior" if dir_arg == '+' else "inferior"

        print(f"\n--- Resultado ---")
        print(f"O limite {tipo_limite} de {funcao} quando x -> {ponto} é: {resultado}")
        
        plot_option = input("Deseja plotar a função para visualização? (s/n): ").lower()
        if plot_option == 's':
            plot_1d_function(funcao, ponto, resultado)

    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Ocorreu um erro com a sua entrada. Verifique a função e o ponto do limite. Detalhes do erro: {e}")

def plot_1d_function(funcao, ponto, resultado):
    """Plota a função de uma variável e marca o ponto do limite."""
    try:
        func_numpy = lambdify(symbols('x'), funcao, 'numpy')
        
        x_vals = np.linspace(float(ponto) - 5, float(ponto) + 5, 400)
        y_vals = func_numpy(x_vals)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(x_vals, y_vals, label=f'f(x) = {funcao}')
        
        ax.set_title(f"Comportamento da função próximo a x = {ponto}")
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.grid(True)
        ax.legend()
        
        # Marca o ponto do limite
        ax.scatter(float(ponto), float(resultado), color='red', s=100, zorder=5, label=f'Limite em ({ponto}, {resultado})')
        
        filename = input("Digite o nome do arquivo para salvar (sem extensão): ")
        save_plot(fig, filename)
        
        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o gráfico: {e}")


def calcular_limite_2d():
    """Calcula limites de uma função de duas variáveis e opcionalmente plota a função."""
    try:
        func_str = input("Digite a função (ex: (x**2 - y**2) / (x**2 + y**2)): ")
        ponto_x_str = input("Digite o ponto do limite para x (ex: 0): ")
        ponto_y_str = input("Digite o ponto do limite para y (ex: 0): ")
        
        x, y = symbols('x y')
        funcao = sympify(func_str)
        ponto_x = sympify(ponto_x_str)
        ponto_y = sympify(ponto_y_str)

        resultado = limit(funcao, (x, y), (ponto_x, ponto_y))
        
        print(f"\n--- Resultado ---")
        print(f"O limite de {funcao} quando (x, y) -> ({ponto_x}, {ponto_y}) é: {resultado}")
        
        plot_option = input("Deseja plotar a função para visualização? (s/n): ").lower()
        if plot_option == 's':
            plot_2d_function(funcao, ponto_x, ponto_y, resultado)

    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Ocorreu um erro com a sua entrada. Verifique a função e o ponto do limite. Detalhes do erro: {e}")

def plot_2d_function(funcao, ponto_x, ponto_y, resultado):
    """Plota a função de duas variáveis e marca o ponto do limite."""
    try:
        x_sym, y_sym = symbols('x y')
        func_numpy = lambdify((x_sym, y_sym), funcao, 'numpy')

        range_val = 2.0
        step = 0.1
        x_grid, y_grid = np.meshgrid(np.arange(float(ponto_x) - range_val, float(ponto_x) + range_val + step, step),
                                     np.arange(float(ponto_y) - range_val, float(ponto_y) + range_val + step, step))
        z_grid = func_numpy(x_grid, y_grid)
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none')
        
        # Marca o ponto do limite
        ax.scatter(float(ponto_x), float(ponto_y), float(resultado), color='red', s=100, zorder=5, label=f'Limite em ({ponto_x}, {ponto_y}, {resultado})')
        
        ax.set_title(f"Comportamento da função próximo a ({ponto_x}, {ponto_y})")
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_zlabel('Eixo Z')
        ax.legend()
        
        filename = input("Digite o nome do arquivo para salvar (sem extensão): ")
        save_plot(fig, filename)
        
        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o gráfico: {e}")

def limite_calculator():
    """Menu principal para o cálculo de limites."""
    while True:
        print("\n--- Calculadora de Limites ---")
        print("Escolha o número de variáveis:")
        print("1. Uma variável (f(x))")
        print("2. Duas variáveis (f(x, y))")
        print("3. Voltar ao menu principal")
        
        choice = input("Sua escolha: ")
        
        if choice == '1':
            calcular_limite_1d()
        elif choice == '2':
            calcular_limite_2d()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    limite_calculator()