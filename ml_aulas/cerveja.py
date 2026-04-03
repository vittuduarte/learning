# %%
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
# %%
df = pd.read_excel('data/dados_cerveja.xlsx')
df.head()
# %%
features = ['temperatura', 'copo', 'espuma', 'cor']
target = ['classe']

X = df[features]
y = df[target]
# %%
X = X.replace({"mud": 1,
           "pint": 2,
           "sim": 1,
           "não": 0,
           "clara": 1,
           "escura": 0
           })
#%%
model = tree.DecisionTreeClassifier()
model.fit(X=X, y=y)
# %%
tree.plot_tree(model,
               feature_names=features,
               class_names=model.classes_,
               filled=True)
# %%
