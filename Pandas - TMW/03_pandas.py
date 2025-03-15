#%%
import pandas as pd
#%%
df = pd.read_csv("../../archive/transacoes.csv")
df.head()

# %%
#Pontos maiores que 50
filtro50 = df["qtdePontos"] >= 50
df[filtro50]
# %%
#Pontos maiores ou iguais a 50 e menores que 100
filtro50e100 = (df["qtdePontos"] >= 50) & (df["qtdePontos"] < 100)
df[filtro50e100]
# %%
#Pontos iguais a 1 ou igual a 100
filtro1ou100 = (df["qtdePontos"] == 1) | (df["qtdePontos"] == 100)
df[filtro1ou100]
# %%
#Pontos entre 0 e 50 ou do ano de 2025
filtro0ou50ano2025 = (df["qtdePontos"] > 0) & (df["qtdePontos"] <= 50) | (df["dtCriacao"] >= '2025-01-01')
df[filtro0ou50ano2025]

# %%
df_prod = pd.read_csv("../../archive/transacao_produto.csv")
df_prod.head()
# %%
filtroIdproduto5ou11 = (df_prod["idProduto"] == 5) | (df_prod["idProduto"] == 11)
df_prod[filtroIdproduto5ou11]
# %%
filtro_Idproduto_5ou11_usando_isin = df_prod["idProduto"].isin([5,11])
df_prod[filtro_Idproduto_5ou11_usando_isin]
# %%
df_clie = pd.read_csv("../../archive/clientes.csv")
df_clie.head()
# %%
#ISNA retorna os valores que sao NaN e o NOTNA retorna os valores que nao sao NaN. Pode-se utilizar o ~ para negar as funcoes, como exemplo ~isna, o retorno seria notna.
filtro_data = df_clie["dtCriacao"].notna()
df_clie[filtro_data]
# %%
