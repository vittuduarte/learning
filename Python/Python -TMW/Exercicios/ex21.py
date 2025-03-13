"""
Faça um programa que receba o nome e a idade de uma pessoa. 

Caso essa pessoa tenha menos de 18 anos, exiba o aviso:
	“Fulano, você não pode dirigir nem beber”

Para as pessoas entre 18 e 65 anos, exiba o aviso:
	“Fulano, bebida liberada! Só não vale dirigir!”

Para as pessoas com mais de 65 anos, exiba o aviso:
	“Fulano, beba com muita moderação!”
"""
#%%
def pode_beber(nome:str, idade:int) -> str:
	if idade >= 18 and idade <= 65:
		print(nome, "bebida liberada! Só não vale dirigir!")
	elif idade < 18:
		print(nome,"você não pode dirigir nem beber")
	else:
		print(nome,"beba com muita moderação!")


nome = input("Digite seu nome.")
nome = str(nome)
idade = input("Digite seu idade.")
idade = int(idade)

pode_beber = pode_beber(nome,idade)
# %%
