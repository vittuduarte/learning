# %%
#Faça o programa de uma sorveteria, onde o usuário pode escolher:
#Tipo de sorvete: casquinha (R$1,00), cascão (R$2,50), cestinha (R$4,00)
#Sabor do sorvete: morango, creme, chocolate
#Cobertura: Caramelo (R$1,50), morango (R$1,50), chocolate (R$1,50), sem cobertura (R$0,00)
#Apresente o valor a ser pago

sorvete = int(input("""Qual o tipo de sorvete você deseja?
                  1 - Casquinha (R$1,00)
                  2 - Cascao (R$2,50)
                  3 - Cestinha (R$4,00)
                  """))

sabores = int(input("""Qual o tipo de sabor voce deseja?
                  1 - Morango
                  2 - Creme
                  3 - Chocolate
                  """))

cobertura = int(input("""Qual o tipo de sabor de cobertura voce deseja?
                  1 - Morango (R$1,50)
                  2 - Caramelo (R$1,50)
                  3 - Chocolate (R$1,50)
                  4 - Sem combertura (R$ 0,00)
                  """))

if sorvete == 1:
    if cobertura == 1 or cobertura == 2 or cobertura == 3:
        valor = 1 * 1.5
        print(f"Valor total e: {valor}")
    elif cobertura == 4:
        valor = 1
        print(f"Valor total e {valor}")
    else:
        print("Sem sortevete, volte mais tarde")
        
if sorvete == 2:
    if cobertura == 1 or cobertura == 2 or cobertura == 3:
        valor = 2.5 * 1.5
        print(f"Valor total e: {valor}")
    elif cobertura == 4:
        valor = 2.5
        print(f"Valor total e {valor}")
        
if sorvete == 3:
    if cobertura == 1 or cobertura == 2 or cobertura == 3:
        valor = 4 * 1.5
        print(f"Valor total e: {valor}")
    elif cobertura == 4:
        valor = 4
        print(f"Valor total e {valor}")
else:
    print("Sem nada")
    
# %%
