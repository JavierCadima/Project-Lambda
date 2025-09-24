-- Lua script para encontrar raízes de uma função usando o método de Newton-Raphson.

local math = require("math")

-- ===================================================================
-- Lógica para ler e compilar a equação
-- ===================================================================

local func_str = arg[1]
local deriv_str = arg[2]
local initial_guess = tonumber(arg[3])
local tolerance = tonumber(arg[4])

if not func_str or not deriv_str or not initial_guess or not tolerance then
    io.stderr:write("Erro: Argumentos insuficientes ou inválidos.\n")
    os.exit(1)
end

-- Dicionário de substituições para o Lua
local substitutions = {
    ['^'] = "math.pow",
    ['ln'] = "math.log",
    ['log'] = "math.log10",
    ['tg'] = "math.tan",
    ['cotg'] = "(1/math.tan)",
    ['sec'] = "(1/math.cos)",
    ['cossec'] = "(1/math.sin)",
    ['sin'] = "math.sin",
    ['cos'] = "math.cos",
    ['tan'] = "math.tan",
    ['asin'] = "math.asin",
    ['acos'] = "math.acos",
    ['atan'] = "math.atan",
    ['exp'] = "math.exp",
    ['sqrt'] = "math.sqrt",
    ['abs'] = "math.abs"
}

-- Realiza as substituições diretamente no script Lua
local function apply_substitutions(str)
    -- Adiciona a conversão de `^` para `math.pow` primeiro para evitar conflitos
    str = str:gsub("([a-zA-Z0-9%.%(%)]+)%^([a-zA-Z0-9%.%(%)]+)", "math.pow(%1, %2)")
    
    for old, new in pairs(substitutions) do
        str = str:gsub(old, new)
    end
    return str
end

func_str = apply_substitutions(func_str)
deriv_str = apply_substitutions(deriv_str)

-- Função segura para carregar e executar strings de código
local function safe_load(source_str)
    -- Cria um ambiente seguro que só permite funções math
    local safe_env = {
        math = math,
        tonumber = tonumber,
        tostring = tostring,
        print = print,
        -- Adicione outras funções necessárias aqui
    }
    setmetatable(safe_env, { __index = _G })

    local chunk, err = load("return function(x) return (" .. source_str .. ") end", nil, "t", safe_env)
    if not chunk then
        io.stderr:write("Erro ao compilar a função: " .. err .. "\n")
        os.exit(1)
    end
    return chunk()
end

local func, err1 = pcall(safe_load, func_str)
if not func then
    io.stderr:write("Erro: Não foi possível carregar a função f(x): " .. err1 .. "\n")
    os.exit(1)
end

local deriv, err2 = pcall(safe_load, deriv_str)
if not deriv then
    io.stderr:write("Erro: Não foi possível carregar a derivada f'(x): " .. err2 .. "\n")
    os.exit(1)
end

-- ===================================================================
-- Método de Newton-Raphson
-- ===================================================================

local max_iterations = 100
local x = initial_guess

for i = 1, max_iterations do
    local y_val = func(x)
    local y_prime_val = deriv(x)
    
    -- Critério de parada: a função se aproxima de zero
    if math.abs(y_val) < tolerance then
        io.stdout:write(string.format("Raiz encontrada em x = %.10f após %d iterações.\n", x, i))
        os.exit(0)
    end
    
    -- Verifica se a derivada é zero (ponto de inflexão, etc.)
    if y_prime_val == 0 then
        io.stderr:write("Erro: Derivada é zero. O método falhou. Tente outra estimativa inicial.\n")
        os.exit(1)
    end

    -- Calcula a próxima aproximação
    local next_x = x - y_val / y_prime_val
    
    -- Verifica a divergência ou oscilação
    if math.abs(next_x - x) < tolerance then
        io.stdout:write(string.format("Convergência atingida em x = %.10f após %d iterações.\n", next_x, i))
        os.exit(0)
    end
    
    x = next_x
end

io.stderr:write("Aviso: O método de Newton-Raphson não convergiu após " .. max_iterations .. " iterações.\n")
os.exit(1)