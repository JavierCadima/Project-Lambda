import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import sympy
from sympy import symbols, lambdify
import os

def solve_and_plot_equation(equation_string):
    """
    Resolve a equação, gera os pontos e plota o gráfico diretamente.
    """
    print("Gerando dados para as curvas de nível com o solver Python...")
    
    range_val = 3.0
    step = 0.1

    try:
        x_sym, y_sym = symbols('x y')
        sympy_equation = sympy.sympify(equation_string)
        func = lambdify((x_sym, y_sym), sympy_equation, 'numpy')
        
        x_grid, y_grid = np.meshgrid(np.arange(-range_val, range_val + step, step),
                                     np.arange(-range_val, range_val + step, step))
        z_grid = func(x_grid, y_grid)

        fig = plt.figure(figsize=(10, 8))
        CS = plt.contour(x_grid, y_grid, z_grid, 10)
        plt.clabel(CS, inline=True, fontsize=8)
        plt.title(f'Curvas de Nível: {equation_string}')
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.grid(True)
        plt.colorbar(CS, label='Valor de Z')
        
        # --- LÓGICA DE SALVAR O GRÁFICO (AGORA FEITA ANTES DE PLOTAR) ---
        save_option = input("\nDeseja salvar o gráfico? (s/n): ").lower()
        if save_option == 's':
            filename = input("Digite o nome do arquivo (sem extensão): ")
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            
            file_path_png = os.path.join(desktop_path, f"{filename}.png")
            file_path_pdf = os.path.join(desktop_path, f"{filename}.pdf")
            
            try:
                fig.savefig(file_path_png, dpi=300)
                print(f"Gráfico salvo como '{file_path_png}' com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar o arquivo PNG: {e}")

            try:
                fig.savefig(file_path_pdf)
                print(f"Gráfico salvo como '{file_path_pdf}' com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar o arquivo PDF: {e}")

        print("Dados gerados com sucesso.")
        print("Exibindo o gráfico...")
        plt.show()
        plt.close(fig)

        return True
    
    except sympy.SympifyError:
        print("\n--- Erro de Sintaxe! ---")
        print("Verifique se a equação está escrita corretamente.")
        return False
    except (TypeError, ValueError, ZeroDivisionError) as e:
        print("\n--- Erro Matemático! ---")
        print(f"Verifique se a operação é válida (ex: raiz de número negativo, logaritmo de zero/negativo).")
        return False
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        return False

def plot_curves_of_level():
    while True:
        equation_input = input("Digite a função (ex: sin(x*y) + cos(x)): z = ")
        if solve_and_plot_equation(equation_input):
            break

if __name__ == '__main__':
    plot_curves_of_level()