"""
Faça um programa que receba um número. Verifique se o número informado é par ou ímpar. Exiba o resultado da seguinte maneira:

O número x é impar
ou
O número x é par
"""
#%%
def par_impar(numero:int):
    if numero % 2 == 0:
        print("Par!")
    else:
        print("Impar!")
        

numero = input("Entre com um numero: ")
numero = int(numero)

par_impar(numero)
# %%
