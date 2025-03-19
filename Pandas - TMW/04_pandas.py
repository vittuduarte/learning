#%%
import pandas as pd
import numpy as np
# %%
df = pd.read_csv("./data/clientes.csv")
df.head()
# %%
#Criando uma nova coluna
df["pontos_100"] = df["qtdePontos"] + 100
df
# %%
#Transformando os dados de uma coluna
df["log_pontos"] = np.log(df["qtdePontos"] + 1)
# %%
#Ordenacao de valores
df.sort_values(by="qtdePontos", ascending=False).head(5)
# %%
df.sort_values(by=["qtdePontos", "pontos_100"], ascending=[False, True]).tail(5)
# %%
#conversao de tipos
df["pontos_100"].astype(np.float32)
# %%
df["dfCriacao"] = df["dtCriacao"].replace({"0000-00-00 00:00:00.000": "2024-02-01 09:00:00.000"})
pd.to_datetime(df["dfCriacao"])
# %%
#Trabalhando com NAs
df.dropna()
df.dropna(how="all") #Precisa de todos os valores NA para essa linha ser excluida. Usando o Any, se houver um NA toda a linha e excluida.
df.dropna(how="all", subset=["qtdePontos"])

#Preenchendo os valores NA
df["qtdePontos"].fillna(0)

#Removendo duplicatas
df.drop_duplicates() #mantem a primeira replica dos dados
df.drop_duplicates(keep="last") #Mantem a ultiam replica dos dados
df.drop_duplicates(subset=["qtdePontos"])