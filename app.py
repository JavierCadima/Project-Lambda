import math
import os
from itertools import product
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def _as_sympy_expr(expr: str):
    return sp.sympify(
        expr,
        locals={
            "e": math.e,
            "pi": math.pi,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "exp": sp.exp,
        },
    )


def _newton_raphson(func_str: str, guess: float, tol: float):
    x = sp.symbols("x")
    func = _as_sympy_expr(func_str)
    deriv = sp.diff(func, x)
    f_num = sp.lambdify(x, func, "numpy")
    df_num = sp.lambdify(x, deriv, "numpy")

    history = []
    current = float(guess)
    for iteration in range(1, 101):
        value = float(f_num(current))
        derivative_value = float(df_num(current))
        next_value = None

        if abs(derivative_value) > 1e-12:
            next_value = current - value / derivative_value

        history.append({
            "iteracao": iteration,
            "x_atual": current,
            "f_x": value,
            "f_linha_x": derivative_value,
            "proximo_x": next_value,
        })

        if abs(value) < tol:
            return {
                "convergiu": True,
                "raiz": current,
                "iteracoes": iteration,
                "mensagem": f"Raiz encontrada em x = {current:.10f}",
                "historico": history,
            }

        if abs(derivative_value) < 1e-12:
            return {
                "convergiu": False,
                "raiz": None,
                "iteracoes": iteration,
                "mensagem": "Derivada próxima de zero; o método falhou.",
                "historico": history,
            }

        current = next_value

    return {
        "convergiu": False,
        "raiz": None,
        "iteracoes": 100,
        "mensagem": "Não convergiu após 100 iterações.",
        "historico": history,
    }


def _limit_1d(expression: str, point: float, direction: str):
    x = sp.symbols("x")
    expr = _as_sympy_expr(expression)
    if direction == "Ambos":
        return sp.limit(expr, x, point)
    if direction == "+":
        return sp.limit(expr, x, point, dir="+")
    if direction == "-":
        return sp.limit(expr, x, point, dir="-")
    return sp.limit(expr, x, point)


def _limit_2d(expression: str, x_point: float, y_point: float):
    x, y = sp.symbols("x y")
    expr = _as_sympy_expr(expression)
    return sp.limit(expr, (x, y), (x_point, y_point))


def _derivative_1d(expression: str, variable_name: str):
    symbol = sp.symbols(variable_name)
    expr = _as_sympy_expr(expression)
    return sp.diff(expr, symbol)


def _derivative_2d(expression: str, variable_name: str):
    x, y = sp.symbols("x y")
    expr = _as_sympy_expr(expression)
    if variable_name == "x":
        return sp.diff(expr, x)
    if variable_name == "y":
        return sp.diff(expr, y)
    raise ValueError("Escolha x ou y para a derivada parcial.")


def _integral_1d(expression: str, variable_name: str, kind: str, lower=None, upper=None):
    symbol = sp.symbols(variable_name)
    expr = _as_sympy_expr(expression)
    if kind == "Indefinida":
        return sp.integrate(expr, symbol)
    return sp.integrate(expr, (symbol, lower, upper))


def _integral_2d(expression: str, x_lower, x_upper, y_lower, y_upper):
    x, y = sp.symbols("x y")
    expr = _as_sympy_expr(expression)
    return sp.integrate(expr, (x, x_lower, x_upper), (y, y_lower, y_upper))


def _extrema_1d(expression: str, variable_name: str):
    symbol = sp.symbols(variable_name)
    expr = _as_sympy_expr(expression)
    deriv = sp.diff(expr, symbol)
    critical_points = sp.solve(sp.Eq(deriv, 0), symbol)
    valid = []
    for point in critical_points:
        if point.is_real is True or point.is_real is None:
            valid.append(point)
    return valid, deriv


def _extrema_2d(expression: str, x_name: str, y_name: str):
    x, y = sp.symbols(f"{x_name} {y_name}")
    expr = _as_sympy_expr(expression)
    fx = sp.diff(expr, x)
    fy = sp.diff(expr, y)
    return sp.solve([sp.Eq(fx, 0), sp.Eq(fy, 0)], (x, y), dict=True)


def _function_value(expression: str, variables_text: str, values_text: str):
    variables = [item.strip() for item in variables_text.split(",") if item.strip()]
    values = [float(value.strip()) for value in values_text.split(",") if value.strip()]
    if len(variables) != len(values):
        raise ValueError("O número de variáveis e valores deve coincidir.")

    symbols_list = sp.symbols(" ".join(variables))
    substitutions = dict(zip(symbols_list, values))
    expr = _as_sympy_expr(expression)
    return expr.subs(substitutions)


def _truth_table(expression: str, variables_text: str):
    variables_list = [item.strip() for item in variables_text.split(",") if item.strip()]
    expr = expression.lower().replace("and", "&").replace("or", "|").replace("not", "~").replace("xor", "^")
    symbols_list = sp.symbols(variables_list)
    parsed_expr = sp.sympify(expr)
    rows = []
    for values in product([False, True], repeat=len(variables_list)):
        subst = dict(zip(symbols_list, values))
        result = bool(parsed_expr.subs(subst))
        row = {name: int(value) for name, value in zip(variables_list, values)}
        row["Resultado"] = int(result)
        rows.append(row)
    return variables_list, rows


def _render_2d_function(expr: str, x_min: float, x_max: float, samples: int = 500):
    x = sp.symbols("x")
    func = sp.lambdify(x, _as_sympy_expr(expr), "numpy")
    x_values = np.linspace(x_min, x_max, samples)
    y_values = np.asarray(func(x_values), dtype=float)

    figure = Figure(figsize=(6, 4), dpi=100)
    axis = figure.add_subplot(111)
    axis.plot(x_values, y_values, color="#4f46e5", linewidth=2)
    axis.axhline(0, color="black", linewidth=0.8, alpha=0.7)
    axis.axvline(0, color="black", linewidth=0.8, alpha=0.7)
    axis.grid(True, alpha=0.25)
    axis.set_title(f"y = {expr}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    return figure


def _render_3d_function(expr: str, x_min: float, x_max: float, y_min: float, y_max: float, samples: int = 70):
    x, y = sp.symbols("x y")
    func = sp.lambdify((x, y), _as_sympy_expr(expr), "numpy")
    x_values = np.linspace(x_min, x_max, samples)
    y_values = np.linspace(y_min, y_max, samples)
    x_grid, y_grid = np.meshgrid(x_values, y_values)
    z_grid = np.asarray(func(x_grid, y_grid), dtype=float)

    figure = Figure(figsize=(6, 5), dpi=100)
    axis = figure.add_subplot(111, projection="3d")
    axis.plot_surface(x_grid, y_grid, z_grid, cmap="viridis", edgecolor="none")
    axis.set_title(f"z = {expr}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_zlabel("z")
    return figure


def _render_level_curves(expr: str, x_min: float, x_max: float, y_min: float, y_max: float, levels: int = 12):
    x, y = sp.symbols("x y")
    func = sp.lambdify((x, y), _as_sympy_expr(expr), "numpy")
    x_values = np.linspace(x_min, x_max, 200)
    y_values = np.linspace(y_min, y_max, 200)
    x_grid, y_grid = np.meshgrid(x_values, y_values)
    z_grid = np.asarray(func(x_grid, y_grid), dtype=float)

    figure = Figure(figsize=(6, 5), dpi=100)
    axis = figure.add_subplot(111)
    contour = axis.contour(x_grid, y_grid, z_grid, levels=levels, cmap="viridis")
    axis.clabel(contour, inline=True, fontsize=8)
    axis.set_title(f"Curvas de Nível: z = {expr}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(True, alpha=0.25)
    return figure


def _render_level_surface(expr: str, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float, z_max: float, threshold: float = 0.25):
    x, y, z = sp.symbols("x y z")
    func = sp.lambdify((x, y, z), _as_sympy_expr(expr), "numpy")
    xs = np.linspace(x_min, x_max, 30)
    ys = np.linspace(y_min, y_max, 30)
    zs = np.linspace(z_min, z_max, 30)
    x_grid, y_grid, z_grid = np.meshgrid(xs, ys, zs, indexing="ij")
    values = np.asarray(func(x_grid, y_grid, z_grid), dtype=float)
    mask = np.abs(values) <= threshold

    fig = Figure(figsize=(6, 5), dpi=100)
    axis = fig.add_subplot(111, projection="3d")
    if np.any(mask):
        axis.scatter(x_grid[mask], y_grid[mask], z_grid[mask], s=8, color="royalblue")
    axis.set_title(f"Superfície de Nível: {expr} = 0")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_zlabel("z")
    return fig


class ProjectLambdaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project Lambda")
        self.geometry("1200x760")
        self.minsize(980, 640)

        icon_path = os.path.join(os.path.dirname(__file__), "icone.ico")
        self._app_icon_path = icon_path if os.path.exists(icon_path) else None
        if self._app_icon_path:
            try:
                self.iconbitmap(self._app_icon_path)
                self.wm_iconbitmap(self._app_icon_path)
                self.iconbitmap(default=self._app_icon_path)
            except Exception:
                pass

        self.themes = {
            "Retro": {
                "window": "#0d1f14",
                "panel": "#143926",
                "panel_alt": "#0b2b1d",
                "foreground": "#b7f7c4",
                "muted": "#a7d7b0",
                "accent": "#7df9a2",
                "accent2": "#46c56f",
                "entry": "#0a1c13",
                "display": "#a6f5b4",
                "display_bg": "#07170d",
                "button": "#1f5035",
                "button_text": "#eaffef",
                "tab": "#122d20",
                "outline": "#2d7a4c",
            },
            "Black": {
                "window": "#0e0e10",
                "panel": "#1a1a1d",
                "panel_alt": "#111214",
                "foreground": "#f2f2f2",
                "muted": "#b8b8be",
                "accent": "#4cc9f0",
                "accent2": "#6ba7ff",
                "entry": "#121316",
                "display": "#e5f3ff",
                "display_bg": "#080a0d",
                "button": "#2e3136",
                "button_text": "#f5f5f5",
                "tab": "#1c1d20",
                "outline": "#40454c",
            },
            "White": {
                "window": "#f3f5f8",
                "panel": "#ffffff",
                "panel_alt": "#eef2f8",
                "foreground": "#1c2430",
                "muted": "#4d5968",
                "accent": "#2d6cdf",
                "accent2": "#5ea0ff",
                "entry": "#ffffff",
                "display": "#0b1220",
                "display_bg": "#edf3ff",
                "button": "#e8edf7",
                "button_text": "#102033",
                "tab": "#ebf0f5",
                "outline": "#d4dce5",
            },
            "Modern": {
                "window": "#f0f5fb",
                "panel": "#edf3fb",
                "panel_alt": "#dfeaf7",
                "foreground": "#1d2530",
                "muted": "#586981",
                "accent": "#5a9dff",
                "accent2": "#7db4ff",
                "entry": "#f8fbff",
                "display": "#1d2d40",
                "display_bg": "#dfeaf9",
                "button": "#e3ecff",
                "button_text": "#1d2d40",
                "tab": "#e7eef9",
                "outline": "#bfd3f4",
            },
            "Dark Modern": {
                "window": "#171b20",
                "panel": "#222a30",
                "panel_alt": "#1a2127",
                "foreground": "#edf1f5",
                "muted": "#b7c2cc",
                "accent": "#8ebeff",
                "accent2": "#63a6ff",
                "entry": "#262f36",
                "display": "#eef6ff",
                "display_bg": "#0e1215",
                "button": "#303b45",
                "button_text": "#f4f9ff",
                "tab": "#1d242b",
                "outline": "#495a68",
            },
        }

        self.current_theme = "Modern"
        self.configure(bg=self.themes[self.current_theme]["window"])

        self.theme_selector = ttk.Combobox(
            self,
            values=["Retro", "Black", "White", "Modern", "Dark Modern"],
            state="readonly",
            width=18,
        )
        self.theme_selector.set(self.current_theme)
        self.theme_selector.bind("<<ComboboxSelected>>", self._on_theme_change)
        self.theme_selector.pack(anchor="ne", padx=14, pady=(12, 0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        self.graphs_tab = ttk.Frame(self.notebook)
        self.calc_tab = ttk.Frame(self.notebook)
        self.logic_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.graphs_tab, text="Gráficos")
        self.notebook.add(self.calc_tab, text="Cálculos")
        self.notebook.add(self.logic_tab, text="Lógica")

        self._build_graphs_tab()
        self._build_calc_tab()
        self._build_logic_tab()
        self._apply_theme(self.current_theme)

    def _on_theme_change(self, event=None):
        theme = self.theme_selector.get()
        self._apply_theme(theme)

    def _apply_theme(self, theme_name: str):
        theme = self.themes[theme_name]
        self.current_theme = theme_name
        self.configure(bg=theme["window"])

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=theme["window"])
        style.configure("TLabel", background=theme["window"], foreground=theme["foreground"])
        style.configure("TLabelframe", background=theme["window"], foreground=theme["foreground"])
        style.configure("TLabelframe.Label", background=theme["window"], foreground=theme["foreground"])
        style.configure("TNotebook", background=theme["window"], borderwidth=0)
        style.configure("TNotebook.Tab", background=theme["tab"], foreground=theme["foreground"], padding=[12, 8])
        style.map("TNotebook.Tab", background=[("selected", theme["panel"]), ("active", theme["panel_alt"])])
        style.configure("TEntry", fieldbackground=theme["entry"], foreground=theme["foreground"], background=theme["panel"])
        style.configure("TCombobox", fieldbackground=theme["entry"], foreground=theme["foreground"], background=theme["panel"])
        style.configure("TButton", background=theme["button"], foreground=theme["button_text"], padding=[12, 8])
        style.map("TButton", background=[("active", theme["accent2"]), ("pressed", theme["accent"])])

        for widget in [self.graphs_tab, self.calc_tab, self.logic_tab, self.notebook]:
            try:
                widget.configure(background=theme["window"])
            except Exception:
                pass

        if hasattr(self, "calc_result_panel"):
            self.calc_result_panel.configure(bg=theme["display_bg"])
        if hasattr(self, "result_text"):
            self.result_text.configure(bg=theme["display_bg"], fg=theme["display"], insertbackground=theme["display"])
        if hasattr(self, "logic_output"):
            self.logic_output.configure(bg=theme["panel"], fg=theme["foreground"], insertbackground=theme["foreground"])
        if hasattr(self, "plot_container"):
            try:
                self.plot_container.configure(bg=theme["panel"])
            except tk.TclError:
                pass

        if hasattr(self, "graph_type"):
            try:
                self.graph_type.configure(background=theme["entry"], foreground=theme["foreground"])
            except tk.TclError:
                pass

    def _build_graphs_tab(self):
        main_frame = ttk.Frame(self.graphs_tab, padding=16)
        main_frame.pack(fill="both", expand=True)

        form = ttk.LabelFrame(main_frame, text="Configuração do gráfico", padding=12)
        form.pack(side="left", fill="y", padx=(0, 12))

        ttk.Label(form, text="Tipo").grid(row=0, column=0, sticky="w", pady=6)
        self.graph_type = ttk.Combobox(form, values=["2D", "3D", "Curvas de Nível", "Superfície de Nível"], state="readonly", width=22)
        self.graph_type.current(0)
        self.graph_type.grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(form, text="Função").grid(row=1, column=0, sticky="w", pady=6)
        self.graph_expr = ttk.Entry(form, width=30)
        self.graph_expr.insert(0, "sin(x) + x/3")
        self.graph_expr.grid(row=1, column=1, padx=8, pady=6)

        ttk.Label(form, text="x min").grid(row=2, column=0, sticky="w", pady=6)
        self.x_min = ttk.Entry(form, width=12)
        self.x_min.insert(0, "-10")
        self.x_min.grid(row=2, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="x max").grid(row=3, column=0, sticky="w", pady=6)
        self.x_max = ttk.Entry(form, width=12)
        self.x_max.insert(0, "10")
        self.x_max.grid(row=3, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="y min").grid(row=4, column=0, sticky="w", pady=6)
        self.y_min = ttk.Entry(form, width=12)
        self.y_min.insert(0, "-3")
        self.y_min.grid(row=4, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="y max").grid(row=5, column=0, sticky="w", pady=6)
        self.y_max = ttk.Entry(form, width=12)
        self.y_max.insert(0, "3")
        self.y_max.grid(row=5, column=1, sticky="w", padx=8, pady=6)

        btn = ttk.Button(form, text="Gerar gráfico", command=self._render_selected_graph)
        btn.grid(row=6, column=0, columnspan=2, pady=(12, 4), sticky="ew")

        self.plot_container = tk.Frame(main_frame, bg=self.themes[self.current_theme]["panel"])
        self.plot_container.pack(side="left", fill="both", expand=True)

        self.plot_canvas = None
        self._render_selected_graph()

    def _build_calc_tab(self):
        main_frame = ttk.Frame(self.calc_tab, padding=16)
        main_frame.pack(fill="both", expand=True)

        left = ttk.LabelFrame(main_frame, text="Operação", padding=12)
        left.pack(side="left", fill="y", padx=(0, 12))

        self.calc_type = ttk.Combobox(
            left,
            values=["Newton-Raphson", "Limite", "Derivada", "Integral", "Extremos", "Valor da função (N variáveis)"],
            state="readonly",
            width=32,
        )
        self.calc_type.current(0)
        self.calc_type.bind("<<ComboboxSelected>>", lambda _event: self._refresh_calc_form())
        self.calc_type.pack(fill="x", pady=(0, 10))

        self.calc_form = ttk.Frame(left)
        self.calc_form.pack(fill="both", expand=True)

        self.calc_button = ttk.Button(left, text="Calcular", command=self._run_calculation)
        self.calc_button.pack(fill="x", pady=(12, 0))

        right = ttk.LabelFrame(main_frame, text="Resultado", padding=12)
        right.pack(side="left", fill="both", expand=True)

        self.calc_result_panel = tk.Frame(right, padx=8, pady=8, bd=2, relief="sunken")
        self.calc_result_panel.pack(fill="both", expand=True)
        self.result_text = scrolledtext.ScrolledText(
            self.calc_result_panel,
            wrap=tk.WORD,
            width=70,
            height=24,
            font=("Segoe UI", 11, "normal"),
            padx=12,
            pady=12,
            bd=0,
        )
        self.result_text.pack(fill="both", expand=True)

        self._refresh_calc_form()

    def _build_logic_tab(self):
        main_frame = ttk.Frame(self.logic_tab, padding=16)
        main_frame.pack(fill="both", expand=True)

        form = ttk.LabelFrame(main_frame, text="Tabela verdade", padding=12)
        form.pack(fill="x", padx=0, pady=0)

        form.configure(relief="flat")

        ttk.Label(form, text="Expressão").grid(row=0, column=0, sticky="w", pady=6)
        self.logic_expr = ttk.Entry(form, width=40)
        self.logic_expr.insert(0, "(A and B) or not C")
        self.logic_expr.grid(row=0, column=1, padx=8, pady=6, sticky="ew")

        ttk.Label(form, text="Variáveis").grid(row=1, column=0, sticky="w", pady=6)
        self.logic_vars = ttk.Entry(form, width=40)
        self.logic_vars.insert(0, "A, B, C")
        self.logic_vars.grid(row=1, column=1, padx=8, pady=6, sticky="ew")

        ttk.Button(form, text="Gerar tabela", command=self._generate_truth_table).grid(row=2, column=0, columnspan=2, pady=(12, 4), sticky="ew")
        form.columnconfigure(1, weight=1)

        result = ttk.LabelFrame(main_frame, text="Resultado", padding=12)
        result.pack(fill="both", expand=True, pady=(12, 0))

        self.logic_output = scrolledtext.ScrolledText(result, wrap=tk.WORD, width=90, height=18)
        self.logic_output.pack(fill="both", expand=True)

    def _clear_plot(self):
        if self.plot_canvas is not None:
            self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = None

    def _render_selected_graph(self):
        try:
            kind = self.graph_type.get()
            expr = self.graph_expr.get().strip()
            x_min = float(self.x_min.get())
            x_max = float(self.x_max.get())
            y_min = float(self.y_min.get())
            y_max = float(self.y_max.get())

            if kind == "2D":
                fig = _render_2d_function(expr, x_min, x_max)
            elif kind == "3D":
                fig = _render_3d_function(expr, x_min, x_max, y_min, y_max)
            elif kind == "Curvas de Nível":
                fig = _render_level_curves(expr, x_min, x_max, y_min, y_max)
            else:
                fig = _render_level_surface(expr, x_min, x_max, y_min, y_max, y_min, y_max)

            self._clear_plot()
            self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            self.plot_canvas.draw()
            self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as exc:
            messagebox.showerror("Erro", f"Não foi possível gerar o gráfico:\n{exc}")

    def _refresh_calc_form(self):
        for child in self.calc_form.winfo_children():
            child.destroy()

        operation = self.calc_type.get()
        rows = []

        if operation == "Newton-Raphson":
            rows = [
                ("Função f(x)", ttk.Entry(self.calc_form, width=30)),
                ("Estimativa inicial", ttk.Entry(self.calc_form, width=20)),
                ("Tolerância", ttk.Entry(self.calc_form, width=20)),
            ]
            rows[0][1].insert(0, "x**2 - 4")
            rows[1][1].insert(0, "1")
            rows[2][1].insert(0, "1e-6")
        elif operation == "Limite":
            rows = [
                ("Função", ttk.Entry(self.calc_form, width=30)),
                ("Ponto", ttk.Entry(self.calc_form, width=20)),
                ("Direção", ttk.Combobox(self.calc_form, values=["Ambos", "+", "-"], state="readonly", width=15)),
            ]
            rows[0][1].insert(0, "sin(x)/x")
            rows[1][1].insert(0, "0")
            rows[2][1].current(0)
        elif operation == "Derivada":
            rows = [
                ("Função", ttk.Entry(self.calc_form, width=30)),
                ("Variável", ttk.Combobox(self.calc_form, values=["x", "y"], state="readonly", width=15)),
            ]
            rows[0][1].insert(0, "x**3 + 2*x")
            rows[1][1].current(0)
        elif operation == "Integral":
            rows = [
                ("Função", ttk.Entry(self.calc_form, width=30)),
                ("Variável", ttk.Entry(self.calc_form, width=15)),
                ("Tipo", ttk.Combobox(self.calc_form, values=["Indefinida", "Definida"], state="readonly", width=20)),
                ("Limite inferior", ttk.Entry(self.calc_form, width=16)),
                ("Limite superior", ttk.Entry(self.calc_form, width=16)),
            ]
            rows[0][1].insert(0, "x**2 + 1")
            rows[1][1].insert(0, "x")
            rows[2][1].current(0)
            rows[3][1].insert(0, "0")
            rows[4][1].insert(0, "1")
        elif operation == "Extremos":
            rows = [
                ("Função", ttk.Entry(self.calc_form, width=30)),
                ("Variável", ttk.Entry(self.calc_form, width=15)),
            ]
            rows[0][1].insert(0, "x**3 - 3*x")
            rows[1][1].insert(0, "x")
        else:
            rows = [
                ("Função", ttk.Entry(self.calc_form, width=30)),
                ("Variáveis", ttk.Entry(self.calc_form, width=25)),
                ("Valores", ttk.Entry(self.calc_form, width=25)),
            ]
            rows[0][1].insert(0, "x**2 + y**2 + z")
            rows[1][1].insert(0, "x, y, z")
            rows[2][1].insert(0, "2, 3, 4")

        for index, (label_text, widget) in enumerate(rows):
            ttk.Label(self.calc_form, text=label_text).grid(row=index, column=0, padx=(0, 8), pady=6, sticky="w")
            widget.grid(row=index, column=1, padx=(0, 4), pady=6, sticky="ew")
            self.calc_form.columnconfigure(1, weight=1)

        self.calc_form_widgets = rows

    def _run_calculation(self):
        operation = self.calc_type.get()
        try:
            text = self.result_text
            text.delete("1.0", tk.END)

            if operation == "Newton-Raphson":
                func_str = self.calc_form_widgets[0][1].get()
                guess = float(self.calc_form_widgets[1][1].get())
                tol = float(self.calc_form_widgets[2][1].get())
                result = _newton_raphson(func_str, guess, tol)
                text.insert(tk.END, f"{result['mensagem']}\n\n")
                text.insert(tk.END, "Iteração | x atual | f(x) | f'(x) | próximo x\n")
                text.insert(tk.END, "-" * 72 + "\n")
                for row in result["historico"]:
                    text.insert(
                        tk.END,
                        f"{row['iteracao']:>8} | {row['x_atual']:.12f} | {row['f_x']:.12f} | {row['f_linha_x']:.12f} | {row['proximo_x'] if row['proximo_x'] is None else row['proximo_x']:.12f}\n",
                    )

            elif operation == "Limite":
                func_str = self.calc_form_widgets[0][1].get()
                point = float(self.calc_form_widgets[1][1].get())
                direction = self.calc_form_widgets[2][1].get()
                result = _limit_1d(func_str, point, direction)
                text.insert(tk.END, f"Resultado: {result}")

            elif operation == "Derivada":
                func_str = self.calc_form_widgets[0][1].get()
                var = self.calc_form_widgets[1][1].get()
                result = _derivative_1d(func_str, var)
                text.insert(tk.END, f"Resultado: {result}")

            elif operation == "Integral":
                func_str = self.calc_form_widgets[0][1].get()
                var = self.calc_form_widgets[1][1].get()
                kind = self.calc_form_widgets[2][1].get()
                lower = self.calc_form_widgets[3][1].get()
                upper = self.calc_form_widgets[4][1].get()
                if kind == "Indefinida":
                    result = _integral_1d(func_str, var, kind)
                else:
                    result = _integral_1d(func_str, var, kind, float(lower), float(upper))
                text.insert(tk.END, f"Resultado: {result}")

            elif operation == "Extremos":
                func_str = self.calc_form_widgets[0][1].get()
                var = self.calc_form_widgets[1][1].get()
                points, deriv = _extrema_1d(func_str, var)
                text.insert(tk.END, f"Derivada: {deriv}\nPontos críticos: {points}")

            else:
                func_str = self.calc_form_widgets[0][1].get()
                vars_text = self.calc_form_widgets[1][1].get()
                values_text = self.calc_form_widgets[2][1].get()
                result = _function_value(func_str, vars_text, values_text)
                text.insert(tk.END, f"Resultado: {result}")

        except Exception as exc:
            text.insert(tk.END, f"Erro: {exc}")

    def _generate_truth_table(self):
        expr = self.logic_expr.get().strip()
        vars_text = self.logic_vars.get().strip()
        try:
            vars_list, rows = _truth_table(expr, vars_text)
            output = []
            output.append(" | ".join(vars_list + ["Resultado"]))
            output.append("-" * (len(vars_list) * 4 + 12))
            for row in rows:
                values = [str(row[name]) for name in vars_list]
                values.append(str(row["Resultado"]))
                output.append(" | ".join(values))
            self.logic_output.delete("1.0", tk.END)
            self.logic_output.insert(tk.END, "\n".join(output))
        except Exception as exc:
            self.logic_output.delete("1.0", tk.END)
            self.logic_output.insert(tk.END, f"Erro: {exc}")


def main():
    app = ProjectLambdaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
