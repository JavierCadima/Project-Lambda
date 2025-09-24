import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import sympy
from sympy import symbols, sympify, lambdify
import os

def plotar_grafico_2d():
    """Plota um gráfico 2D de uma função y = f(x)."""
    while True:
        try:
            equation_input = input("Digite a função (ex: sin(x) + cos(x)): y = ")
            if not equation_input:
                continue

            print("Gerando dados para o gráfico 2D com o solver Python...")

            x_sym = symbols('x')
            sympy_equation = sympify(equation_input)
            func = lambdify(x_sym, sympy_equation, 'numpy')

            x_vals = np.linspace(-10, 10, 400)
            y_vals = func(x_vals)

            fig = plt.figure(figsize=(8, 6))
            plt.plot(x_vals, y_vals)
            plt.title(f'Gráfico 2D da Função: y = {equation_input}')
            plt.xlabel('Eixo X')
            plt.ylabel('Eixo Y')
            plt.grid(True)
            
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