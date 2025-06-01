#Faça um programa que receba o raio de uma circunferência em centímetros. Retorne para o usuário qual é a área e o perímetro desta circunferência no seguinte formato.
#Área:  x.xx
#Perímetro:  y.yy
#%%
from math import pi

user_area = input("Digite qual o raio que voce deseja calcular? (Digite o numero na unidade de medida centimetros)")
user_area = float(user_area)

c = 2 * pi * user_area
c_formatado = format(c, '.2f')
print(f"O perimetro de {user_area} e: ", c_formatado)
# %%
