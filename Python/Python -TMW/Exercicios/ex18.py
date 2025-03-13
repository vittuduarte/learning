#Faça um programa que receba dois valores A e B. Faça a soma desses dois valores e retorne o resultado:
#Soma:  x.xx
#%%
def soma_numero(num_a: float, num_b:float) -> float:
    return num_a + num_b

num_a = input("Digite um numero: ")
num_b = input("Digite um numero: ")
num_a = float(num_a)
num_b = float(num_b)

resultado = soma_numero(num_a=num_a, num_b=num_b)
print(f"A soma dos numeros e: {resultado}")
    
# %%
