from numpy.random import randn
import pandas as pd

df = pd.Dataframe(randn(2, 3), index=["a","b","c","d","e"], columns="W X Y Z".split())
df

#Acessando valores no dataframe
df["W"]
df[["W", "Y"]]

#Criando nova coluna
df["new"] = df["W"] + df["Y"]

#Excluindo valores
df.drop("new")
df.drop("new", axis=1)
df.drop("new", axis=1, inplace=True) #Utilizado para excluir a coluna (axis =1 colunas, axis=0 linhas)

#Acessando valores
df.loc["a"] #Utilizado para acessar as linhas
df.iloc[0,2] #Utilizado para percorrer  linhas e colunas
df.iloc[:-1:1:4]
df > 0 #Selecao condicional, retorna um dataframe boolean
df[df>0] #selecao condicional, retorna um dataframe com NaN onde a condicional nao for verdadeira
df[df["Y"] > 0] #Retorna um dataframe somente com a condicao baseada em Y for verdadeira

#Nomes das linhas e colunas
df.index 
df.columns

#operacoes
df.info()
df.memory_usage()
df["W"].unique() #Mostra os valores unicos de uma coluna
df["W"].nunique() #Mostra o tamanho da lista de valores unicos de uma coluna
df["W"].value_counts() #Mostra os valores unicos e seus valores
df["W"].apply(lambda x: x.values) #Executa uma funcao em todos os valores da coluna
df["Novo W"] = df["W"].apply(lambda x: x.values) #Cria uma nova coluna com os valores alterados da coluna W
df.map()
df.pivot_table(index="a", columns="W", values="d")

#Criando index
df.reset_index()
df.set_index("index")

#Lidando com valores faltantes
df.dropna()
df.fillna()
df.ffill()
df.bfill()

#Agrupamento
df.groupby()
df.groupby(["class1", "class2"]).sum()
df.groupby.sum()
df.groupby.mean()
df.groupby.min()
df.groupby.max()
df.groupby.std()
df.groupby.product()
df.groupby.idxmax()


#Concat
pd.concat([df,df2,df3])
pd.concat([df,df2,df3],axis=1) #Linhas iguas
pd.concat([df,df2,df3],axis=0) #Colunas iguais

#Merge
pd.merge(df,df2, on=["Key"])
pd.merge(df,df2, on=["Key", "Key2"])
pd.merge(df,df2, how="outer", on=["Key", "Key2"])
pd.merge(df,df2, how="inner", on=["Key", "Key2"])
pd.merge(df,df2, how="right", on=["Key", "Key2"])
pd.merge(df,df2, how="left", on=["Key", "Key2"])

#Join
df.join(df2)
df.join(df2, how="left")

