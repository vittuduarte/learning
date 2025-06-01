# %%
#Altere o programa anterior para considerar a quantidade de água
texto = """
Qual garrafa de agua voce gostaria de comprar?
(1) - Agua mineral sem gas (R$ 1,50)
(2) - agua mineral com gas (R$ 2,50)
"""
opcao = input(texto)

qtde = int(input("quantas garrafas? "))

if opcao == '1':
    result = qtde * 1.5
    print(f"O valor total deu {result}")
else:
    result = qtde * 2.5
    print(f"O valor total deu {result}")
# %%
