# %%
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

# %%
df = pd.read_parquet("data/dados_clones.parquet")
df.head(10)
# %%

X = df.drop(columns=["Status "])
y = df["Status "]
# %%
categorical_coluns = X.select_dtypes(include="object").columns
encoder = OneHotEncoder(handle_unknown='ignore',
                        sparse_output=False)
# %%
X_encoded = encoder.fit_transform(X[categorical_coluns])
feature_names = encoder.get_feature_names_out(categorical_coluns)
X_enc = pd.DataFrame(X_encoded, columns=feature_names)


# %%
model = tree.DecisionTreeClassifier(random_state=42)
# %%
model.fit(X=X_enc, y=y)
# %%
tree.plot_tree(model,
               feature_names=X_enc.columns,
               class_names=model.classes_,
               filled=True,
               max_depth=3)
