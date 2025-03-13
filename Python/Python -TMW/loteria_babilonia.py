"""
Construa um programa que realiza o sorteio de um numero entre 1 e 15.
O usuario tera 3 chances de acertar o valor
A cada tentativa voce deve informar se o chute e maior ou menor que o numero sorteado
Caso o usuario acerte, de os parabens    
"""
#%%
import random

def get_input() -> str:
    while True:
        try:
            numero_usuario = int(input("Entre com o um numero: "))
        except ValueError as err:
            print("Entre com um numero valido")
            continue
        
        if not 1 <= numero_usuario <= 15:
            break
        
        print("Valor invalido, O valor deve ser entre 1 e 15")

def check_numbers(usuario:int, sorteio:int) -> str:
    if usuario == sorteio:
        print("Parabens! Acertou mizera!")
        return True
    elif sorteio > usuario:
        print("Numero muito alto. Tente um numero menor!")
        return False
    else:
        print("Numero muito baixo. Tente um numero maior!")
        return False


numero_sorteio = random.randint(1,15)

for i in range(0,3):
    
    numero_usuario = get_input()
    if check_numbers(usuario=numero_usuario, sorteio=numero_sorteio):
        break
else:
    print("Suas tentativas acabaram!")