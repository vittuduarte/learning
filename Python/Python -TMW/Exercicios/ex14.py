#Faça um programa que receba 4 alturas, armazene em uma lista e depois mostre a soma dessas alturas.
#%%
soma = 0
qdte_entradas = 1

while qdte_entradas <= 4:
    altura = input("Digite as alturas: ")
    altura = float(altura)
    soma += altura
    qdte_entradas += 1
print(f"Soma total das alturas: {soma}")
# %%
