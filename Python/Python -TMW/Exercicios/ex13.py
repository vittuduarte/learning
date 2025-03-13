#Faça um programa que conte quantas vezes a letra “a” aparece em uma palavra
#%%
palavra = input("Digite uma palavra qualquer: ").lower()

contador = 0
for i in palavra:
    if i == "a":
        contador += 1
    
print(f"A letra 'a' apareceu em {palavra}, {contador} vezes.")
# %%
