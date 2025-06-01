#%%
import pandas as pd
import os
# %%
df_geral = pd.read_csv("./data/ipea/homicidios.csv", sep=";")
df_geral = df_geral.rename(columns={"valor":"homicidios"})
df_geral.head()
# %%
df_negros = pd.read_csv("./data/ipea/homicidios-negros.csv", sep=";")
df_negros = df_negros.rename(columns={"valor":"homicidios"})
df_negros.head()
# %%
df_geral = df_geral.set_index(["nome", "período"])
df_negros = df_negros.set_index(["nome", "período"])
# %%
pd.concat([df_geral, df_negros], axis=1)
# %%
#criando uma funcao para melhorar a concatenacao geral
def read_file(file_name:str) -> pd.DataFrame:
    df = (
        pd.read_csv(f"./data/ipea/{file_name}.csv", sep=";")
        .rename(columns={"valor":file_name})
        .set_index(["nome", "período"])
        .drop(["cod"], axis=1)
    )
    return df
    

df_negros = read_file("homicidios-negros")
df_negros
# %%
#utilizando o OS para navegar pelo diretorio
file_name = os.listdir("./data/ipea/")
file_name
# %%
dfs = []
for i in file_name:
    file_name = i.split(".")[0]
    dfs.append(read_file(file_name))
# %%
df_completo = (pd.concat(dfs, axis=1)
                .reset_index()
                .sort_values(["período", "nome"]))
# %%
df_completo
# %%
#salvado o arquivo
df_completo.to_csv("./data/ipea/homicidios_consolidado.csv", index=False, sep=";")
# %%
