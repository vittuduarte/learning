# %%
""" Escreva uma função chamada triangle que receba uma string e um número inteiro
    e desenhe um triangulo com altura especificada, composto de multiplas copias da string."""
def triangle(word, line) -> str:
    x = 0
    for x in range(1, line + 1):
        print(f'{word * x}')

triangle('l', 5)

#%%
""" Escreva uma função chamada rectangle que receba uma string e dois números inteiros 
    e desenhe um retangulo com altura e largura especificada, composto de multiplas copias da string."""
def rectangle(word, width, length) -> str:
    print(word * width)
    
    for _ in range(length):
        print(word * (length) + word)

    if length > 1:
        print(word * width)

rectangle('H', 5, 4)

#%%
""" a musica "99 Bottles of Beer" tem uma letra que se repete, mudando apenas o número de garrafas. 
    Escreva um programa que imprima a letra da musica, para 99 garrafas, e depois para 98, e assim por diante, até chegar a 0.
    
    Exemplo:
    99 bottles of beer on the wall,
    99 bottles of beer.
    Take one down and pass it around, 
    98 bottles of beer on the wall.
"""
def bottle_verse(number):
    for garrafas_atuais in range(number, 0, -1):
        print(f'{garrafas_atuais} bottles of beer on the wall,')
        print(f'{garrafas_atuais} bottles of beer.')
        print('Take one down and pass it around,')
        
        new = garrafas_atuais - 1
        print(f'{new} bottles of beer on the wall.\n')

bottle_verse(99)
# %%
