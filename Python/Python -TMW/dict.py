#%%
#dados chave-valor
exp = {"nome": "Victor",
       "sobrenome": "Duarte",
       "Filhos": False,
       "Formacao": ["BSc Ciencia da Computacao",
                    "Esp. Big Data e Data Science",
                    "MSc. Informatica"],
       "Cargos":[ 
           {"nome": "Estagiario", "Empresa": "Escolas IDAAM"},
           {"nome": "Tecnico de TI", "Empresa": "Dodo Veiculos"},
           {"nome": "Analista de Negocio", "Empresa": "Hiroshima"},
           {"nome": "Pesquisador Graduado", "Empresa": "Motorola"},
           {"nome": "Tecnico de TI", "Empresa": "IF-AM"}]
       }

print(exp)
# %%
print(exp["Formacao"][-1])
# %%
print(exp["Cargos"][-1]["Empresa"])
# %%
#Adicionando chaves no dict
exp["Estado civil"] = "solteiro"
print(exp)
# %%
#Saber o nome das chaves presentes no dict
exp.keys()
# %%
#Saber os valores presentes no dict
exp.values()
# %%
#Saber os pares chave-valor de um dict
exp.items()
# %%
#Percorrendo os dados dentro de um dict
for i in exp:
    print(i, "->", exp[i])
# %%
for i in exp.items():
    print(i)
# %%
for chave, valor in exp.items(): #[chave, valor]
    print(chave, "->", valor)
# %%
