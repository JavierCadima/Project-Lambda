import sympy
from sympy import symbols, sympify, diff, lambdify
import numpy as np

def newton_raphson_solver(func_str, guess, tolerance):
    """
    Executa o método de Newton-Raphson para encontrar a raiz de uma função.
    """
    print("Executando o método de Newton-Raphson em Python...")

    try:
        x_sym = symbols('x')
        funcao = sympify(func_str)
        
        # Calcula a derivada simbolicamente
        derivada = diff(funcao, x_sym)

        # Converte as expressões simbólicas em funções numéricas para cálculo rápido
        func = lambdify(x_sym, funcao, 'numpy')
        deriv = lambdify(x_sym, derivada, 'numpy')

        # Converte a estimativa e a tolerância para números
        x = float(guess)
        tol = float(tolerance)  # <-- Esta é a linha corrigida

        max_iterations = 100
        
        for i in range(max_iterations):
            y_val = func(x)
            y_prime_val = deriv(x)

            # Critério de parada: a função se aproxima de zero
            if np.abs(y_val) < tol:
                print(f"Raiz encontrada em x = {x:.10f} após {i} iterações.")
                return x

            # Verifica se a derivada é zero (ponto de inflexão, etc.)
            if y_prime_val == 0:
                print("Erro: Derivada é zero. O método falhou. Tente outra estimativa inicial.")
                return None

            # Calcula a próxima aproximação
            x = x - y_val / y_prime_val

        print(f"Aviso: O método não convergiu após {max_iterations} iterações.")
        return None

    except sympy.SympifyError:
        print("\n--- Erro de Sintaxe! ---")
        print("Verifique se a função está escrita corretamente.")
        return None
    except (ValueError, TypeError, ZeroDivisionError) as e:
        print(f"\n--- Erro na Entrada! ---")
        print(f"Verifique se a função, a estimativa e a tolerância estão corretas. Detalhes: {e}")
        return None

def newton_raphson_calculator():
    """
    Interface para o usuário usar o método de Newton-Raphson.
    """
    while True:
        func_input = input("Digite a função (ex: x**2 - 4): f(x) = ")
        guess = input("Digite sua estimativa inicial: ")
        tolerance = input("Digite a tolerância desejada (ex: 1e-6): ")

        result = newton_raphson_solver(func_input, guess, tolerance)
        if result is not None:
            break