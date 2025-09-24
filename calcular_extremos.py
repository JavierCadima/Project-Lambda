import sympy
from sympy import symbols, sympify, diff, solve, lambdify
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

def encontrar_extremos_1d():
    """Calcula os pontos críticos (máximo e mínimo) para uma função f(x) e opcionalmente plota o resultado."""
    try:
        func_str = input("Digite a função f(x): ")
        var_name = input("Digite a variável (ex: x): ")

        variavel = symbols(var_name)
        funcao = sympify(func_str)
        
        # Calcula a primeira derivada
        derivada = diff(funcao, variavel)
        
        # Encontra os pontos críticos (onde a derivada é zero)
        pontos_criticos = solve(derivada, variavel)
        
        if not pontos_criticos:
            print("\nNão foram encontrados pontos críticos.")
            return

        print(f"\n--- Pontos Críticos ---")
        pontos_criticos_reais = []
        for ponto in pontos_criticos:
            # Filtra apenas pontos críticos reais para plotagem
            if ponto.is_real:
                pontos_criticos_reais.append(ponto)
            
            valor_funcao = funcao.subs(variavel, ponto)
            print(f"Ponto crítico em x = {ponto}")
            print(f"Valor da função neste ponto: f({ponto}) = {valor_funcao}\n")
        
        if pontos_criticos_reais:
            plot_option = input("Deseja plotar o gráfico? (s/n): ").lower()
            if plot_option == 's':
                plot_1d_extremos(funcao, variavel, pontos_criticos_reais)
        else:
            print("Não há pontos críticos reais para plotagem.")
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique a função e a variável de entrada. Detalhes: {e}")

def plot_1d_extremos(funcao, variavel, pontos_criticos):
    """Plota a função de uma variável e marca os pontos críticos."""
    try:
        func_numpy = lambdify(variavel, funcao, 'numpy')

        # Define um intervalo para o gráfico
        x_min = min(float(ponto.evalf()) for ponto in pontos_criticos) - 2 if pontos_criticos else -5
        x_max = max(float(ponto.evalf()) for ponto in pontos_criticos) + 2 if pontos_criticos else 5
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = func_numpy(x_vals)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(x_vals, y_vals, label=f'f({variavel}) = {funcao}')
        
        for ponto in pontos_criticos:
            x_ponto = float(ponto.evalf())
            y_ponto = float(funcao.subs(variavel, ponto).evalf())
            ax.scatter(x_ponto, y_ponto, color='red', s=100, zorder=5)
            ax.text(x_ponto, y_ponto, f'  ({x_ponto:.2f}, {y_ponto:.2f})', fontsize=9, ha='left', va='bottom')
        
        ax.set_title(f"Gráfico da função e seus pontos críticos")
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

def encontrar_extremos_2d():
    """Calcula os pontos críticos (máximo, mínimo ou ponto de sela) para uma função f(x, y) e opcionalmente plota o resultado."""
    try:
        func_str = input("Digite a função f(x, y): ")
        x_name = input("Digite a primeira variável (ex: x): ")
        y_name = input("Digite a segunda variável (ex: y): ")
        
        x, y = symbols(x_name), symbols(y_name)
        funcao = sympify(func_str)
        
        # Calcula as derivadas parciais de primeira ordem
        fx = diff(funcao, x)
        fy = diff(funcao, y)
        
        # Encontra os pontos críticos resolvendo o sistema fx = 0 e fy = 0
        pontos_criticos = solve([fx, fy], (x, y))
        
        if not pontos_criticos:
            print("\nNão foram encontrados pontos críticos.")
            return

        print(f"\n--- Pontos Críticos ---")
        if isinstance(pontos_criticos, dict):
            # Se for um único ponto
            valor_funcao = funcao.subs({x: pontos_criticos[x], y: pontos_criticos[y]})
            print(f"Ponto crítico em ({x_name}, {y_name}) = ({pontos_criticos[x]}, {pontos_criticos[y]})")
            print(f"Valor da função neste ponto: f({pontos_criticos[x]}, {pontos_criticos[y]}) = {valor_funcao}\n")
        else:
            # Se forem múltiplos pontos
            for ponto in pontos_criticos:
                x_val, y_val = ponto
                valor_funcao = funcao.subs({x: x_val, y: y_val})
                print(f"Ponto crítico em ({x_name}, {y_name}) = ({x_val}, {y_val})")
                print(f"Valor da função neste ponto: f({x_val}, {y_val}) = {valor_funcao}\n")
        
        plot_option = input("Deseja plotar o gráfico? (s/n): ").lower()
        if plot_option == 's':
            plot_2d_extremos(funcao, pontos_criticos, x, y)
            
    except (sympy.SympifyError, ValueError, TypeError) as e:
        print(f"\n--- Erro! ---")
        print(f"Verifique a função e as variáveis de entrada. Detalhes: {e}")

def plot_2d_extremos(funcao, pontos_criticos, x_sym, y_sym):
    """Plota a superfície da função de duas variáveis e marca os pontos críticos."""
    try:
        func_numpy = lambdify((x_sym, y_sym), funcao, 'numpy')

        range_val = 5.0
        step = 0.2
        x_grid, y_grid = np.meshgrid(np.arange(-range_val, range_val + step, step),
                                     np.arange(-range_val, range_val + step, step))
        z_grid = func_numpy(x_grid, y_grid)

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none', alpha=0.8)
        
        # Marca os pontos críticos
        if isinstance(pontos_criticos, dict):
            # Se for um único ponto
            x_ponto = float(pontos_criticos[x_sym].evalf())
            y_ponto = float(pontos_criticos[y_sym].evalf())
            z_ponto = float(funcao.subs({x_sym: x_ponto, y_sym: y_ponto}).evalf())
            ax.scatter(x_ponto, y_ponto, z_ponto, color='red', s=100, zorder=5, label='Ponto Crítico')
        else:
            # Se forem múltiplos pontos
            for ponto in pontos_criticos:
                x_ponto = float(ponto[0].evalf())
                y_ponto = float(ponto[1].evalf())
                z_ponto = float(funcao.subs({x_sym: x_ponto, y_sym: y_ponto}).evalf())
                ax.scatter(x_ponto, y_ponto, z_ponto, color='red', s=100, zorder=5)
        
        ax.set_title(f'Gráfico 3D da Função: z = {funcao}')
        ax.set_xlabel(f'Eixo {x_sym}')
        ax.set_ylabel(f'Eixo {y_sym}')
        ax.set_zlabel('Eixo Z')
        ax.legend()

        filename = input("Digite o nome do arquivo para salvar (sem extensão): ")
        save_plot(fig, filename)
        
        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o gráfico: {e}")

def main():
    """Menu principal para o cálculo de máximos e mínimos."""
    while True:
        print("\n--- Calculadora de Máximos e Mínimos ---")
        print("Escolha o tipo de função:")
        print("1. f(x) (uma variável)")
        print("2. f(x, y) (duas variáveis)")
        print("3. Sair")
        
        escolha = input("Sua escolha: ")
        
        if escolha == '1':
            encontrar_extremos_1d()
        elif escolha == '2':
            encontrar_extremos_2d()
        elif escolha == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    main()