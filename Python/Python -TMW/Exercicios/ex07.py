# %%
#Faça um programa que vende uma garrafa de água:
#Se o cliente escolher água mineral natural, será cobrado R$1,50
#Se o cliente escolher água mineral com gás, será cobrado R$2,50


intro = int(input("""
Qual garrafa de agua voce gostaria de comprar?
1 - Agua mineral sem gas
2 - agua mineral com gas
"""
))

if intro == 1:
    print("Valor total da comrpa e R$ 1.50")
elif intro == 2:
    print("Valor total da compra 1 R$2,50")
else:
    print("Valor da opcao invalida!")
# %%
intro = int(input("""
Qual garrafa de agua voce gostaria de comprar?
1 - Agua mineral sem gas
2 - agua mineral com gas
"""
))

conta = 0

if intro == 1:
    conta = 1.5
elif intro == 2:
    conta = 2.5
if conta == 0:
    print("Valor da opcao invalida!")
else:
    print(f"Sua conta deu: R$ {conta}")


# %%
