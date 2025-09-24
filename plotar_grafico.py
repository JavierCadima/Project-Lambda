import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy
from sympy import symbols, sympify, lambdify
import os

def plot_superficiedenivel():
    """Plota um gráfico 3D de uma superfície de nível definida por uma equação implícita."""
    while True:
        try:
            equation_input = input("Digite a equação da superfície (ex: x**2 + y**2 + z**2 - 1): ")
            if not equation_input:
                continue

            print("Gerando dados para o gráfico 3D com o solver Python...")

            x_sym, y_sym, z_sym = symbols('x y z')
            sympy_equation = sympify(equation_input)
            func = lambdify((x_sym, y_sym, z_sym), sympy_equation, 'numpy')

            range_val = 2.0
            step = 0.05
            x_grid, y_grid, z_grid = np.meshgrid(np.arange(-range_val, range_val + step, step),
                                                  np.arange(-range_val, range_val + step, step),
                                                  np.arange(-range_val, range_val + step, step))

            vals = func(x_grid, y_grid, z_grid)
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            ax.set_title(f'Gráfico 3D da Superfície: {equation_input}')
            ax.set_xlabel('Eixo X')
            ax.set_ylabel('Eixo Y')
            ax.set_zlabel('Eixo Z')

            ax.contour(x_grid, y_grid, vals, [0], colors='blue')
            ax.contour(x_grid, z_grid, vals, [0], colors='red')
            ax.contour(y_grid, z_grid, vals, [0], colors='green')

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
            print("Verifique se a equação está escrita corretamente.")
        except Exception as e:
            print(f"\n--- Erro! ---")
            print(f"Ocorreu um erro ao processar ou plotar a equação: {e}")