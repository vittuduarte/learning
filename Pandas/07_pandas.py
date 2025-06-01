#%%
import pandas as pd
# %%
df_transacoes = pd.read_csv("./data/transacoes.csv")
df_transacoes.head()
# %%
df_transacoes_produto = pd.read_csv("./data/df_transacoes_produto.csv")
df_transacoes_produto.head()
# %%
df_produtos = pd.read_csv('./data/produtos.csv')
df_produtos.head()

#%%
#Exercício

cliente_transacao_produto = df_transacoes.merge(
    right=df_transacoes_produto, 
    how='left', 
    on='idTransacao',
)

cliente_transacao_produto = cliente_transacao_produto[['IdTransacao', 'idCliente', 'idProduto']]

#%%
df_full = cliente_transacao_produto.merge(
    df_produtos,
    on=['idProduto'],
    how='left',
)
#%%
df_full = df_full[df_full["descProduto"] == "Presença Streak"]
df_full

#%%
(df_full.groupby(by=["idCliente"])["idTransacao"]
    .count()
    .sort_values(ascending=False)
    .head(1)
 
 )

#%%
#Fazendo de maneira fast-and-furious
produtos = df_produtos[df_produtos["descProduto"]=="Presença Streak"]

(df_transacoes.merge(right=df_transacoes_produto, how='left', on='idTransacao',)
                       .merge(produtos, on=["idProduto"], how="right")
                       .groupby(by="idCliente")["idTransacao"]
                       .count()
                       .sort_values(ascending=False)
                       .head(1)
)