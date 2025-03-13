#%%
nome_arquivo = "shrek.txt"

open_file = open(nome_arquivo, "r")

conteudo = open_file.read()
print(conteudo)

open_file.close()

# %%
#Melhor maneira de ler arquivos.
with open(nome_arquivo) as open_file:
    conteudo = open_file.read()
    
print(conteudo)
# %%

#Escrever no arquivo
txt = "Essa historia tem continuacao!"

with open(nome_arquivo, mode="a") as open_file:
    conteudo = open_file.write(txt)
    
print(conteudo)

#%%
#Exemplo de manipulacao de dados
arquivo = "exemplo.csv"

with open(arquivo) as open_file:
    lines = open_file.readlines()
    
for l in lines:
    print(l)
    
# %%
dados = dict()

chaves = lines[0].strip("\n").split(";")
for chave in chaves:
    dados[chave] = []
# %%
for l in lines[1:]:
    valores = l.strip("\n").split(";")
    for i in range(0, len(valores)):
        dados[chaves[i]].append(valores[i])
print(dados)
# %%
