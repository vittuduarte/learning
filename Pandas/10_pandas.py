#%%
import pandas as pd
# %%
df = pd.read_csv("./data/ipea/homicidios_consolidado.csv", sep=";")
df.head()
# %%
#Escolhendo qual as colunas base
df_stack = (df.set_index(["nome", "período"])).stack()
#empilhando os dados, mas o returno vai ser uma series
#para retornar igual dataframe e necessario usar o comando reset_index()
df_stack = df_stack.reset_index()
#
df_stack.columns = ["nome", "período", "metrica", "valor"]
df_stack
# %%
#Desempilhando os dados
df_unstack = (df_stack.set_index(["nome", "período", "metrica"])
                .unstack()
                .reset_index()
            )
# %%
df_unstack
# %%
df_unstack.columns
# %%
metricas = df_unstack.columns.droplevel(0)[2:].tolist()
df_unstack.columns = ["nome", "período"] + metricas
df_unstack
# %%

#Usando Pivot table
df_stack.pivot_table(values="valor", 
                     index=["nome", "período"], 
                     columns="metrica")
# %%
# retornando para o original
(df_stack.pivot_table(values="valor", 
                     index=["nome", "período"], 
                     columns="metrica")).reset_index()
# %%
df_stack.pivot_table(values="valor",
               index=["nome"],
               columns="metrica",
               aggfunc='mean')