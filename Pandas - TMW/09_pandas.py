#%%
import pandas as pd
import sqlalchemy
from sklearn import cluster
# %%
#Criando a conexao com o banco de dados.
engine = sqlalchemy.create_engine("sqlite:///../data/olist.db")

clientes = pd.read_sql_table(table_name="tb_customers", con=engine)

#%%
clientes.shape

#%%
query = "SELECT * FROM tb_customers LIMIT 100"

df_100 = pd.read_sql_query(query, con=engine)
df_100

#%%
# Lendo um arquivo que possua SQL para criar a query.
with open("etl.sql") as open_file:
    query = open_file.read()

print(query)

#%%
#exemplo criando uma nova informacao na tabela.
kmean = cluster.KMeans(n_clusters=4)
kmean.fit(df_100[["totalRevenue", "qtSalles"]])

df_100["cluster"] = kmean.labels_
df_100

#%%
#Enviando os novos dados para o banco de dados.
df_100.to_sql("sellers_cluster", 
              con=engine, 
              index=False,
              if_exists="replace")