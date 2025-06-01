#Faça um programa que verifique se o item que a pessoa escolheu para comprar na loja está na lista: laranja, cerveja, miojo, carvão, picanha.

#%%
itens_loja = ["Laranja", "Cerveja", "Miojo", "Carvao", "Picanha"]

pedido = input("Qual item voce gostaria de comprar? ")

if pedido in itens_loja:
    print("Temos o item: ", pedido)
else:
    print("Desculpe, nao temos este item no momento.")
# %%
