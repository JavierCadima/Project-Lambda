<p align="center">
  <img src="https://github.com/user-attachments/assets/3e7d91be-64a4-47c0-a856-37902621231b" alt="Project Lambda Logo" width="200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14.2-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-In%20Development-orange.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-Open%20Source-green.svg" alt="License">
</p>

<p align="center">
  <a href="#portugues">Português</a> •
  <a href="#english">English</a> •
  <a href="#espanol">Español</a>
</p>

# Project Lambda

Project Lambda e um Sistema de Apoio Computacional educacional e de codigo aberto criado no Brasil para fins didaticos. O software foi projetado para auxiliar estudantes, professores e pesquisadores na resolucao, calculo e visualizacao grafica de topicos de Calculo I, Calculo II, Metodos Numericos e Logica Matematica.

A aplicacao possui uma interface grafica responsiva desenvolvida em Tkinter com suporte a temas visuais dinamicos, motor de computacao simbolica e plotagem grafica interativa.

Status do Projeto: Em Desenvolvimento
Versao do Python: 3.14.2
Licenca: Open Source

[Portugues](https://www.google.com/search?q=%23portugues) | [English](https://www.google.com/search?q=%23english) | [Espanol](https://www.google.com/search?q=%23espanol)

---

## Portugues

Bem-vindo ao repositorio do Project Lambda!

O Project Lambda e um SAC educacional e open-source projetado para computacao matematica e visualizacao de dados. A aplicacao utiliza o arquivo app.py para a execucao da interface grafica principal.

### Estrutura do Projeto

```text
project-lambda/
├── app.py              -- Interface Grafica Principal (Tkinter/TTK) e Motores de Calculo
├── icone.ico           -- Icone da Aplicacao
└── README.md           -- Documentacao do Projeto

```

### Funcionalidades

#### 1. Visualizacao Grafica

* Graficos 2D: Plotagem de funcoes cartesianas y = f(x).
* Graficos 3D: Visualizacao de superficies tridimensionais z = f(x, y).
* Curvas de Nivel: Geracao de isolinhas para funcoes de duas variaveis.
* Superficies de Nivel: Representacao em malha espacial para equacoes f(x, y, z) = 0.

#### 2. Calculo Numérico e Simbolico

* Metodo de Newton-Raphson: Determinacao de raizes numericas com relatorio passo a passo de iteracoes.
* Limites (1D e 2D): Calculo de limites unilaterais (+ ou -) e bilaterais.
* Derivadas: Derivacao simbolica ordinaria e parcial em relacao a variavel escolhida.
* Integrais: Integrais definidas com limites de integracao e integrais indefinidas.
* Extremos de Funcoes: Localizacao de pontos criticos onde a derivada e nula.
* Avaliacao Multivariavel: Substitucao de variaveis por valores numericos em expressoes com N variaveis.

#### 3. Logica Matematica

* Tabela Verdade: Geracao automatica de tabelas-verdade a partir de expressoes logicas utilizando os operadores AND, OR, NOT e XOR.

#### 4. Personalizacao Visuais

* Suporte a alternancia dinamica de temas: Retro, Black, White, Modern e Dark Modern.

### Requisitos e Tecnologias

* Linguagem: Python 3.14.2
* Interface Grafica: tkinter / ttk
* Computacao e Computacao Grafica: numpy, sympy, matplotlib

### Como Usar e Executar

#### 1. Instalacao de Dependencias

```bash
pip install numpy sympy matplotlib

```

#### 2. Execucao da Aplicacao

```bash
python app.py

```

#### 3. Gerando o Executavel com PyInstaller

Para empacotar a aplicacao e sua interface grafica (app.py) em um arquivo executavel standalone no Windows, execute no terminal ou PowerShell:

```powershell
pyinstaller app.py --name lambda --onefile --windowed --icon "icone.ico"

```

---

## English

Welcome to the Project Lambda repository!

Project Lambda is an educational, open-source Computer Support System (SAC) created in Brazil. It serves as an interactive platform for students and educators to calculate, analyze, and visualize core topics in Calculus I & II, Numerical Methods, and Mathematical Logic.

The project relies on the app.py file to launch the main graphical interface.

### Project Structure

```text
project-lambda/
├── app.py              -- Main Graphical User Interface (Tkinter/TTK) & Computing Engines
├── icone.ico           -- Application Icon
└── README.md           -- Project Documentation

```

### Features

#### 1. Graphical Visualization

* 2D Plotting: Rendering Cartesian functions y = f(x).
* 3D Plotting: Three-dimensional surface rendering z = f(x, y).
* Contour Lines: Generation of level curves for multivariable functions.
* Level Surfaces: Spatial 3D mesh rendering for implicit equations f(x, y, z) = 0.

#### 2. Numerical and Symbolic Calculus

* Newton-Raphson Method: Numerical root finding with full step-by-step iteration logs.
* Limits (1D & 2D): Computation of one-sided (+ or -) and two-sided limits.
* Derivatives: Symbolic ordinary and partial differentiation.
* Integrals: Definite integration with user-defined boundaries and indefinite integration.
* Extrema Finding: Identification of critical points where the derivative vanishes.
* Multivariable Evaluation: Variable substitution and expression evaluation across N variables.

#### 3. Mathematical Logic

* Truth Table Generator: Automated generation of truth tables from logical expressions using AND, OR, NOT, and XOR operators.

#### 4. Custom Themes

* Dynamic theme switching support: Retro, Black, White, Modern, and Dark Modern.

### Requirements & Tech Stack

* Language: Python 3.14.2
* GUI Framework: tkinter / ttk
* Scientific Libraries: numpy, sympy, matplotlib

### How to Use and Run

#### 1. Installing Dependencies

```bash
pip install numpy sympy matplotlib

```

#### 2. Running the Application

```bash
python app.py

```

#### 3. Building the Executable with PyInstaller

To package the GUI application (app.py) and its icon into a single standalone executable file on Windows, run in PowerShell or Terminal:

```powershell
pyinstaller app.py --name lambda --onefile --windowed --icon "icone.ico"

```

---

## Espanol

Bienvenido al repositorio del Project Lambda!

Project Lambda es un Sistema de Apoyo Computacional (SAC) educativo y de codigo abierto desarrollado en Brasil. Ha sido disenado como una plataforma interactiva para estudiantes y docentes con el fin de calcular, analizar y visualizar conceptos clave de Calculo I y II, Metodos Numericos y Logica Matematica.

El proyecto utiliza el archivo app.py para ejecutar la interfaz grafica principal.

### Estructura del Proyecto

```text
project-lambda/
├── app.py              -- Interfaz Grafica Principal (Tkinter/TTK) y Motores de Calculo
├── icone.ico           -- Icono de la Aplicacion
└── README.md           -- Documentacion del Proyecto

```

### Caracteristicas

#### 1. Representacion Grafica

* Graficos 2D: Renderizado de funciones cartesianas y = f(x).
* Graficos 3D: Superficies tridimensionales z = f(x, y).
* Curvas de Nivel: Generacion de isolineas para funciones de dos variables.
* Superficies de Nivel: Mallas espaciales tridimensionales para ecuaciones f(x, y, z) = 0.

#### 2. Calculo Numerico y Simbolico

* Metodo de Newton-Raphson: Busqueda de raices numericas con registro detallado de iteraciones.
* Limites (1D y 2D): Calculo de limites laterales (+ o -) y bilaterales.
* Derivadas: Derivacion simbolica ordinaria y parcial.
* Integrales: Integrales definidas con limites de integracion e integrales indefinidas.
* Puntos Extremos: Localizacion de puntos criticos.
* Evaluacion Multivariable: Sustitucion de variables y evaluacion de expresiones en N variables.

#### 3. Logica Matematica

* Generador de Tablas de Verdad: Creacion automatica de tablas de verdad a partir de expresiones logicas con operadores AND, OR, NOT y XOR.

#### 4. Temas Personalizables

* Soporte para cambio dinamico de interfaz: Retro, Black, White, Modern y Dark Modern.

### Requisitos y Tecnologias

* Lenguaje: Python 3.14.2
* Interfaz Grafica: tkinter / ttk
* Librerias Cientificas: numpy, sympy, matplotlib

### Instalacion y Uso

#### 1. Instalacion de Dependencias

```bash
pip install numpy sympy matplotlib

```

#### 2. Ejecucion de la Aplicacion

```bash
python app.py

```

#### 3. Generar Ejecutable con PyInstaller

Para empaquetar la aplicacion con su interfaz grafica (app.py) y el icono en un ejecutable unico para Windows, ejecute en la consola:

```powershell
pyinstaller app.py --name lambda --onefile --windowed --icon "icone.ico"

```

---

## Autor

Desenvolvido por Javier Cadima.
