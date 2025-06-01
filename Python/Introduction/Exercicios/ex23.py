"""
    Escreva um programa que solicite ao usuario frases. Para parar de solicitar frases, ele pode apenas apertar enter.
    Seu programa deve apresentar cada frase e quantas vezes ela foi repetida.
"""
#%%

#Dict que armazena as frases do user
dados = {}

#Loop para entrada de dados do user
while True:
    frase = input("Entre com a frase desejada: ")
    if frase == "":
        break

    #Adicionando as dados ao dict vazio
    if frase not in dados:
        dados[frase] = 1
    else:
        dados[frase] += 1
        
#Exibir quantas vezes a frase foi vista no dict
for i in dados:
    print(i, "->", dados[i])