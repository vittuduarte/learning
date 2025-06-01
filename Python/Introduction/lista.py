# %%
#Maneira de definir uma lista.
idades = [28,42,43,35,29,39,22]

print(idades)
print("Primeiro elemento da lista: ", idades[0])
print("Dois primeiros elementos", idades[0:2]) #[:2]
print("Dois ultimos elementos", idades[3:5]) #[-2:]
print("Pulando os elementos da lista de 2 em 2", idades[::2]) #[::2]
print("Max idade: ", max(idades))
print("Min idade: ", min(idades))
print("Qtde idade: ", len(idades))
print("Media idade: ", sum(idades)/len(idades))
# %%
