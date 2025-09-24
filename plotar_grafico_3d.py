import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy
from sympy import symbols, sympify, lambdify
import os

def plot_function3d():
    """Plota um gráfico 3D de uma função z = f(x, y)."""
    while True:
        try:
            equation_input = input("Digite a função (ex: sin(x) + cos(y)): z = ")
            if not equation_input:
                continue

            print("Gerando dados para o gráfico 3D com o solver Python...")

            x_sym, y_sym = symbols('x y')
            sympy_equation = sympify(equation_input)
            func = lambdify((x_sym, y_sym), sympy_equation, 'numpy')

            range_val = 3.0
            step = 0.1
            x_grid, y_grid = np.meshgrid(np.arange(-range_val, range_val + step, step),
                                         np.arange(-range_val, range_val + step, step))

            z_grid = func(x_grid, y_grid)

            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none')
            ax.set_title(f'Gráfico 3D da Superfície: z = {equation_input}')
            ax.set_xlabel('Eixo X')
            ax.set_ylabel('Eixo Y')
            ax.set_zlabel('Eixo Z')

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

            print("Exibindo o gráfico...")
            plt.show()
            plt.close(fig)
            break

        except sympy.SympifyError:
            print("\n--- Erro de Sintaxe! ---")
            print("Verifique se a função está escrita corretamente.")
        except Exception as e:
            print(f"\n--- Erro! ---")
            print(f"Ocorreu um erro ao processar ou plotar a equação: {e}")