# %%
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
# %%
df = pd.read_excel('data/dados_frutas.xlsx')
df.head()
# %%
arvore = tree.DecisionTreeClassifier(random_state=42)

# %%
caracteristicas = ['Arredondada', 'Suculenta', 'Vermelha', 'Doce']
y = df['Fruta']
X = df[caracteristicas]
# X = df.drop('Fruta', axis=1)
# %%
arvore.fit(X, y)
# %%
arvore.predict([[1, 1, 0, 1]])
# %%
tree.plot_tree(arvore,
               feature_names=caracteristicas,
               class_names=arvore.classes_,
               filled=True)
# %%
proba = arvore.predict_proba([[1, 1, 0, 1]])
pd.Series(proba[0], index=arvore.classes_)

# %%
