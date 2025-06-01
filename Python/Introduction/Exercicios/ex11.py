#Faça um programa que verifique se a pessoa pertence à família “calvo” ou “silva”.
#%%
nome = input("Digite seu nome: ")
f1 = "calvo"
f2 = "silva"
if nome == f1:
    print(f"Parabens, voce e da familia {f1}!")
elif nome == f2:
    print(f"Parabens, voce e da familia {f2}!")
else:
    print(f"voce nao faz parte da familia!")
# %%
