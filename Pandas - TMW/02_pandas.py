#%%
import pandas as pd
# %%
#importando dados CSV
df = pd.read_csv('./data/clientes.csv')
df
# %%
#salvando arquivos csv, parquet
df.to_csv("clientes.csv", index=False)
df.to_parquet("clientes.parquet", index=False)
df.to_excel("clientes.xlsx", index=False)
# %%
url = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
dfs = pd.read_html(url)
dfs
# %%
df_uf = dfs[1]
df_uf.to_csv("ufs.csv", index=False, sep=";")
# %%
df_uf
# %%
