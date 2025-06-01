#%%
# Selecionando a primeira transacao diaria de cada usuario.
import pandas as pd
# %%
transacoes = pd.read_csv("./data/transacoes.csv")
transacoes
# %%
transacoes = transacoes.sort_values(by="dtCriacao")
transacoes
# %%
transacoes["data"] = pd.to_datetime(transacoes["dtCriacao"]).dt.date
transacoes.drop_duplicates(keep="first", subset=["idCliente", "data"])
# %%
