#Classes e Objetos
#%%
lista = [1,2,3,4,5]

# %%
print(type(lista))
# %%
lista.append(6)
# %%
print(lista)
# %%
class exemplo():
    pass
# %%
x = exemplo()
# %%
print(type(x))
# %%
class cachorro():
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


# %%
dog = cachorro('Rex', 5)
# %%
print(dog.nome)
# %%
print(dog.idade)
# %%
class circulo():
    def __init__(self, raio):
        self.raio = raio

    def area(self):
        return 3.14 * (self.raio ** 2)

    def perimetro(self):
        return 2 * 3.14 * self.raio
# %%
c = circulo(5)
# %%
print(c.area())
# %%
print(c.perimetro())
# %%
#Herança
class animal():
    def __init__(self, nome):
        print('Animal criado')
        self.nome = nome

    def falar(self):
        pass
# %%