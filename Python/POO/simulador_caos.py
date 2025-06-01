#%%
import random
import seaborn as sns
# %%
class academia():
    def __init__(self):
        self.halteres = [i for i in range(10, 36) if i % 2 == 0]
        self.porta_halteres = {}
        self.reiniciar_o_dia()

    def reiniciar_o_dia(self):
        self.porta_halteres = {i: i for i in self.halteres} 

    def listar_halteres(self):
        return [i for i in self.porta_halteres.values() if i != 0]
    
    def lista_espacos(self):
        return [i for i, j in self.porta_halteres.items() if j == 0]
    
    def pegar_halteres(self, peso):
        halt_pos = list(self.porta_halteres.values()).index(peso)
        key_halter = list(self.porta_halteres.keys())[halt_pos]
        self.porta_halteres[key_halter] = 0
        return peso
    
    def devolver_halteres(self, pos, peso):
        self.porta_halteres[pos] = peso


    def calcula_caos(self):
        num_caos = [i for i, j in self.porta_halteres.items() if i != j]
        return len(num_caos) / len(self.porta_halteres) * 100


class usuario():
    def __init__ (self, tipo, academia):
        self.tipo = tipo
        self.academia = academia
        self.peso = 0

    def iniciar_treino(self):
        self.peso = random.choice(self.academia.listar_halteres())
        self.academia.pegar_halteres(self.peso)

    def finalizar_treino(self):
        espacos = self.academia.lista_espacos()

        if self.tipo == 1:
            if self.peso in espacos:
                self.academia.devolver_halteres(self.peso, self.peso)
            else:
                pos = random.choice(espacos)
                self.academia.devolver_halteres(pos, self.peso)


        if self.tipo == 2:
            pos = random.choice(espacos)
            self.academia.devolver_halteres(pos, self.peso)
        self.peso = 0

# %%
academia = academia()

usuarios = [usuario(1, academia) for i in range(10)]
usuarios += [usuario(2, academia) for i in range(1)]
random.shuffle(usuarios)
# %%
list_caos = []

for k in range(50):
    academia.reiniciar_o_dia()
    for i in range(10):
        random.shuffle(usuarios)
        for usuario in usuarios:
            usuario.iniciar_treino()
        for usuario in usuarios:
            usuario.finalizar_treino()
    list_caos += [academia.calcula_caos()]
# %%
sns.displot(list_caos)
# %%
