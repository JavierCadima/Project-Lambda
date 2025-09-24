import sympy
from sympy import symbols, sympify, integrate, lambdify
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
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

def calcular_integral_1d():
    """Calcula integrais de uma variável e opcionalmente plota o resultado."""
    try:
        func_str = input("Digite a função a ser integrada: ")
        var_name = input("Digite a variável de integração: ")
        
        variavel = symbols(var_name)
        funcao = sympify(func_str)
        
        tipo_integral = input("Tipo de integral (indefinida/definida): ").lower()
        
        if tipo_integral.startswith("i"):
            integral = integrate(funcao, variavel)
            print(f"\n--- Resultado (Indefinida) ---")
            print(f"A integral de {funcao} em relação a {variavel} é: {integral} + C")

            plot_option = input("Deseja plotar a integral? (s/n): ").lower()
            if plot_option == 's':
                plot_1d_integral(funcao, integral, variavel)
        
        elif tipo_integral.startswith("d"):
            limite_inf_str = input("Limite inferior: ")
            limite_sup_str = input("Limite superior: ")
            
            limite_inf = sympify(limite_inf_str)
            limite_sup = sympify(limite_sup_str)
            
            integral = integrate(funcao, (variavel, limite_inf, limite_sup))
            print(f"\n--- Resultado (Definida) ---")
            print(f"A integral de {funcao} de {limite_inf} a {limite_sup} é: {integral}")
            
        else:
            print("Escolha inválida. Por favor, digite 'indefinida' ou 'definida'.")
            return
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique se a função, a variável e os limites estão corretos. Detalhes do erro: {e}")

def plot_1d_integral(funcao, integral, variavel):
    """Plota a função original e sua integral indefinida em um gráfico 2D."""
    try:
        func_numpy = lambdify(variavel, funcao, 'numpy')
        integral_numpy = lambdify(variavel, integral, 'numpy')

        x_vals = np.linspace(-10, 10, 400)
        y_vals = func_numpy(x_vals)
        y_integral_vals = integral_numpy(x_vals)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(x_vals, y_vals, label=f'f({variavel}) = {funcao}')
        ax.plot(x_vals, y_integral_vals, label=f"∫ f({variavel})d{variavel} = {integral}", linestyle='--')
        
        ax.set_title(f"Gráfico de f({variavel}) e sua Integral Indefinida")
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

def calcular_integral_2d():
    """Calcula integrais duplas de uma função de duas variáveis."""
    try:
        func_str = input("Digite a função a ser integrada (f(x, y)): ")
        
        x, y = symbols('x y')
        funcao = sympify(func_str)
        
        print("\n--- Limites de Integração ---")
        x_lim_inf = input("Limite inferior para x: ")
        x_lim_sup = input("Limite superior para x: ")
        y_lim_inf = input("Limite inferior para y: ")
        y_lim_sup = input("Limite superior para y: ")
        
        integral = integrate(funcao, (x, sympify(x_lim_inf), sympify(x_lim_sup)),
                                    (y, sympify(y_lim_inf), sympify(y_lim_sup)))
        
        print(f"\n--- Resultado (Integral Dupla) ---")
        print(f"A integral dupla de {funcao} em dA é: {integral}")
        print("\nNão é possível plotar o resultado de uma integral dupla, pois ele é um único valor numérico.")
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique se a função e os limites estão corretos. Detalhes do erro: {e}")

def calcular_integral():
    """Menu principal para o cálculo de integrais."""
    while True:
        print("\n--- Calculadora de Integrais ---")
        print("Escolha o número de variáveis:")
        print("1. Uma variável (Integral simples)")
        print("2. Duas variáveis (Integral dupla)")
        print("3. Voltar ao menu principal")
        
        choice = input("Sua escolha: ")
        
        if choice == '1':
            calcular_integral_1d()
        elif choice == '2':
            calcular_integral_2d()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    calcular_integral()