#%%
import math
""" O volume de uma esfera com raio r é dado pela fórmula V = 4/3 * pi * r^3. 
    Qual é o volume de uma esfera com raio de 5 centímetros? """
r = 5 # raio da esfera em centimetros
volume = (4 / 3) * math.pi * r ** 3 # fórmula do volume de uma esfera em centimetros cubicos
print(volume)
# %%
""" Desenvolva esse código, (cos x)^2 + (sin x)^2,
    para mostrar que o resultado é sempre 1, independentemente do valor de x.
"""
x = 42
formula = (math.cos(x))**2 + (math.sin(x))**2
print(formula)
# %%
""" Utilize as funções sen e cos para calcular o seno e o cosseno de x, e a soma de seus quadrados.
    O resultado deve ser proximo de 1. Pode nao ser exatamente 1 porque a aritmetica de ponto flutuante não é exata."""
    
x = 29.5
seno = math.sin(x)
cosseno = math.cos(x)
soma_dos_quadrados = seno**2 + cosseno**2
print(soma_dos_quadrados)

# %%
print(math.e**2)
# %%
print(math.pow(math.e, 2))
# %%
print(math.exp(2))
# %%
