#%%
import pandas as pd
import numpy as np
# %%
df = pd.read_csv("./data/clientes.csv")
# %%
df
# %%
#Aplicar metodos e transformacoes linha a linha
def get_last_id(idcliente:str) -> str:
    return idcliente.split("-")[-1]

df['idCliente'].apply(get_last_id)
# %%
dfs = pd.read_csv("./ufs.csv", sep=";")
dfs
# %%
def str_to_float(x:str) -> float:
    x = float(x.replace(" ", "")
              .replace(",", ".")
              .replace("\xa0", ""))
    return x

# %%
dfs["Área (km²)"] = dfs["Área (km²)"].apply(str_to_float)
dfs["População (Censo 2022)"] = dfs["População (Censo 2022)"].apply(str_to_float)
dfs["PIB (2015)"] = dfs["PIB (2015)"].apply(str_to_float)
dfs["PIB per capita (R$) (2015)"] = dfs["PIB per capita (R$) (2015)"].apply(str_to_float)
# %%
def uf_to_regiao(uf):
    if uf in ["Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"]:
        return "Centro-Oeste"
    elif uf in ["Alagoas","Bahia", "Ceará", "Maranhão", "Paraíba", "Pernambuco", "Piauí", "Rio Grande do Norte", "Sergipe"]:
        return "Nordeste"
    elif uf in ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins"]:
        return "Norte"
    elif uf in ["Espírito Santo","Minas Gerais", "Rio de Janeiro", "São Paulo"]:
        return "Sudeste"
    elif uf in ["Paraná", "Rio Grande do Sul", "Santa Catarina"]:
        return "Sul"
    
dfs["Região"] = dfs["Unidade federativa"].apply(uf_to_regiao)
# %%
def mortalidade_to_float(x:str):
    x = float(x.replace("‰", "")
               .replace(",", ".")
              )
    return x

dfs["Mortalidade infantil (/1000)"] = dfs["Mortalidade infantil (2016)"].apply(mortalidade_to_float)

#%%
def classifica_bom(linha):
    return (linha["PIB per capita (R$) (2015)"] > 30000 and
            linha["Mortalidade infantil (/1000)"] < 15 and 
            linha["IDH (2010)"] > 700)

dfs.apply(classifica_bom, axis=1)

# %%

dfs.apply(lambda x: x["PIB per capita (R$) (2015)"], axis=1)