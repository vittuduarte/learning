#%%
import pandas as pd
import numpy as np
# %%
df_transacoes = pd.read_csv("./data/transacoes.csv")
df_transacoes
# %%
df_transacoes.groupby(by=["idCliente"]).count()
# %%
#Em formato de serie
df_transacoes.groupby(by=["idCliente"])["idTransacao"].count()
# %%
#Em formato de dataframe
df_transacoes.groupby(by=["idCliente"])[["idTransacao"]].count()
# %%
summary = (df_transacoes.groupby(by=["idCliente"], as_index=False)
              .agg({"idTransacao": ['count'],
                    "qtdePontos": ['sum', 'mean']})
                )
# %%
#acessando os valores nesse novo dataframe agregado
summary.columns
# %%
summary[("qtdePontos", "mean")]
# %%
summary.columns = ["idCliente", "qtdeTransacao", "totalPontos", "avgPontos"]
summary
# %%
def diff_amp(x: pd.Series) -> int:
    amplitude = x.max() - x.min()
    media = x.mean()
    return np.sqrt((amplitude - media)**2)
# %%
(df_transacoes.groupby(by=["idCliente"], as_index=False)
              .agg({"idTransacao": ['count'],
                    "qtdePontos": ['sum', 'mean', diff_amp]})
                )
# %%
#Tempo de vida do usuario dentro do sistema
def life_time(x: pd.Series) -> int:
    dt = pd.to_datetime(x)
    return (dt.max() - dt.min()).days

(df_transacoes.groupby(by=["idCliente"], as_index=False)
              .agg({"idTransacao": ['count'],
                    "qtdePontos": ['sum', 'mean', diff_amp],
                    "dtCriacao": [life_time]
                    })
                )
# %%
