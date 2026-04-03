# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
# %%
df = pd.read_excel("data/dados_cerveja_nota.xlsx")
df
# %%
X = df[["cerveja"]]
y = df["nota"]
# %%
regressao = linear_model.LinearRegression(fit_intercept=True)
regressao.fit(X, y)
# %%
# valores de coeficientes A e B da equação da reta
a, b = regressao.intercept_, regressao.coef_[0]
# %%
plt.scatter(X, y)
plt.grid(True)
plt.plot(X, regressao.predict(X), color="red")
plt.xlabel("Cerveja")
plt.ylabel("Nota")
plt.legend(["Observacoes", f'y={a:.3f}+{b:.3f} * x'])
plt.show()
# %%
