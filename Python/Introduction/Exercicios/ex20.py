"""
Faça um programa que receba um número em segundos, converta esse número para horas, minuto e segundos. Exemplos:
Entrada: 556
Saída: 0:9:16

Entrada: 140153
Saída: 38:55:53
"""

def transforma_numero(numero:int) -> str:
    horas = numero // (60 * 60) #horas inteiras
    minutos = numero // 60 #minutos inteiros
    segundos = numero % (60 * 60) # resto de segundos da divisao por hora
    segundos = numero % 60 # resto de segundos da divisao por minuto
    
    return (f"{horas}:{minutos}:{segundos}")


numero_user = input("Digite um numero: ")
numero_user = int(numero_user)

resultado = transforma_numero(numero=numero_user)
print(resultado)