#%%
import pandas as pd
# %%
idades = [
    32,38,30,30,31,
    35,25,29,31,37,
    27,23,36,33,32,
]

idades
# %%
#Media e variancia utilizando listas
media_idade = sum(idades) / len(idades)
print("Media de idades: ", media_idade)
# %%
diffs = 0
for i in idades:
    diffs += (i - media_idade) ** 2
    
variancia = diffs / (len(idades) - 1)
print("Variancia de idades: ", variancia)
# %%
#Media e variancia utilizando Pandas
series_idades = pd.Series(idades)
series_idades
# %%
print("Media usando Pandas: ",series_idades.mean())
print("Variancia usando Pandas: ",series_idades.var())
# %%
summary_idades = series_idades.describe()
summary_idades
# %%
#Index em Series Pandas, utilizado para navegação em Series.
series_idades.iloc[0] #Utilizado para navegar nas posições e não no index.
series_idades.loc[32] #Utilizado para navegar no Index.
# %%
idades = [
    32,38,30,30,31,
    35,25,29,31,37,
    27,23,36,33,39,
]

indexs = [
    "Alice", "Bernardo", "Carolina", "Diego", "Eduarda",
    "Felipe", "Gabriela", "Henrique", "Isabela", "João",
    "Laura", "Marcelo", "Natália", "Otávio", "Patrícia",
]

series_idades = pd.Series(idades, index=indexs)
series_idades
# %%
#Mexendo com Dataframes
idades = [
    32,38,30,30,31,
    35,25,29,31,37,
    27,23,36,33,39,
]

nomes = [
    "Alice", "Bernardo", "Carolina", "Diego", "Eduarda",
    "Felipe", "Gabriela", "Henrique", "Isabela", "João",
    "Laura", "Marcelo", "Natália", "Otávio", "Patrícia",
]

df = pd.DataFrame()
df["idades"] = idades
df["nomes"] = nomes
df
# %%
#acessando valores no dataframe
df["nomes"]
df.iloc[0]
df.iloc[0]["nomes"]
df.iloc[-1]["idades"]
# %%
