#%%
import requests
import json
from tqdm import tqdm
import pandas as pd

ceps = ["69090150", "69055230", "69025010", "69080900"]

url = "https://viacep.com.br/ws/{cep}/json/"

dados = []
for i in tqdm(ceps):
    resposta = requests.get(url.format(cep=i))
    if resposta.status_code == 200:
        dados.append(resposta.json())

dados
# %%
with open("ceps.json", "w") as open_file:
    json.dump(dados, open_file, ensure_ascii=False, indent=4)
# %%
#Usando Pandas para salvar em csv
dataset = pd.DataFrame(dados)
dataset.to_csv("ceps.csv", sep=";", index=False)