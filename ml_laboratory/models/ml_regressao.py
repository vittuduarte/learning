"""
================================================================================
MACHINE LEARNING — REGRESSÃO
Problema: Previsão de Preço de Imóveis (California Housing Dataset)
================================================================================

ETAPAS COBERTAS:
  1. Carregamento e entendimento dos dados
  2. Análise exploratória (EDA)
  3. Pré-processamento e feature engineering
  4. Divisão treino/teste
  5. Treinamento de múltiplos modelos
  6. Avaliação e comparação de modelos
  7. Otimização de hiperparâmetros
  8. Serialização (pkl) e inferência em novos dados

Bibliotecas: scikit-learn, pandas, numpy, matplotlib, seaborn, joblib
================================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    mean_absolute_percentage_error
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
MODEL_PATH = Path("modelo_regressao.pkl")
np.random.seed(SEED)

print("=" * 70)
print("  REGRESSÃO — PREVISÃO DE PREÇO DE IMÓVEIS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 1 — CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/8] Carregando dados...")

np.random.seed(SEED)
n_samples = 2000

# Simular dataset de imóveis com features realistas
renda_mediana    = np.random.exponential(scale=3.5, size=n_samples).clip(0.5, 15)
idade_casa       = np.random.randint(1, 52, size=n_samples).astype(float)
media_quartos    = np.random.normal(5.0, 1.5, size=n_samples).clip(1, 15)
media_banheiros  = np.random.normal(1.1, 0.2, size=n_samples).clip(0.5, 5)
populacao        = np.random.randint(200, 3500, size=n_samples).astype(float)
media_moradores  = np.random.normal(3.0, 1.0, size=n_samples).clip(1, 10)
latitude         = np.random.uniform(32.5, 42.0, size=n_samples)
longitude        = np.random.uniform(-124.5, -114.0, size=n_samples)

# Preço simulado com relações realistas
preco = (
    renda_mediana * 0.35
    + (52 - idade_casa) * 0.008
    + media_quartos * 0.05
    - media_moradores * 0.04
    + np.random.normal(0, 0.15, size=n_samples)
).clip(0.3, 5.5)

df = pd.DataFrame({
    "MedInc":     renda_mediana,
    "HouseAge":   idade_casa,
    "AveRooms":   media_quartos,
    "AveBedrms":  media_banheiros,
    "Population": populacao,
    "AveOccup":   media_moradores,
    "Latitude":   latitude,
    "Longitude":  longitude,
    "MedHouseVal": preco,
})

print(f"  Shape: {df.shape}")
print(f"  Features: {list(df.columns[:-1])}")
print(f"  Target: MedHouseVal (valor mediano em $100k)")
print(f"\n  Primeiras linhas:\n{df.head(3).to_string()}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 2 — ANÁLISE EXPLORATÓRIA (EDA)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/8] Análise Exploratória...")

print(f"\n  Estatísticas descritivas:")
print(df.describe().round(2).to_string())

print(f"\n  Valores ausentes:")
print(df.isnull().sum().to_string())

# Correlação com o target
correlacoes = df.corr()["MedHouseVal"].sort_values(ascending=False)
print(f"\n  Correlação com o preço:")
print(correlacoes.round(3).to_string())

# Plot: distribuição do target + correlação
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("EDA — Preços de Imóveis (California)", fontsize=14, fontweight="bold")

axes[0].hist(df["MedHouseVal"], bins=50, color="#2196F3", edgecolor="white", alpha=0.8)
axes[0].set_title("Distribuição do Preço")
axes[0].set_xlabel("Valor Mediano ($100k)")
axes[0].set_ylabel("Frequência")

corr_matrix = df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            ax=axes[1], linewidths=0.5, annot_kws={"size": 7})
axes[1].set_title("Matriz de Correlação")

plt.tight_layout()
plt.savefig("regressao_eda.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: regressao_eda.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 3 — FEATURE ENGINEERING & PRÉ-PROCESSAMENTO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/8] Feature Engineering e Pré-processamento...")

# Criar novas features
df["rooms_per_household"]   = df["AveRooms"] / df["AveOccup"]
df["bedrooms_ratio"]        = df["AveBedrms"] / df["AveRooms"]
df["population_per_household"] = df["Population"] / df["HouseAge"]

print("  Novas features criadas: rooms_per_household, bedrooms_ratio, population_per_household")

# Separar features e target
feature_cols = [col for col in df.columns if col != "MedHouseVal"]
X = df[feature_cols]
y = df["MedHouseVal"]

print(f"  Total de features: {X.shape[1]}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 4 — DIVISÃO TREINO/TESTE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/8] Dividindo dados (80% treino / 20% teste)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED
)
print(f"  Treino: {X_train.shape[0]} amostras | Teste: {X_test.shape[0]} amostras")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 5 — PIPELINE DE PRÉ-PROCESSAMENTO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/8] Treinando e comparando modelos...")

# Pipeline genérico: imputer + scaler
preprocessor = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

# Dicionário de modelos candidatos
modelos = {
    "Regressão Linear":    Pipeline([("pre", preprocessor), ("model", LinearRegression())]),
    "Ridge (L2)":          Pipeline([("pre", preprocessor), ("model", Ridge(alpha=1.0))]),
    "Lasso (L1)":          Pipeline([("pre", preprocessor), ("model", Lasso(alpha=0.01))]),
    "Random Forest":       Pipeline([("pre", preprocessor), ("model", RandomForestRegressor(n_estimators=100, random_state=SEED))]),
    "Gradient Boosting":   Pipeline([("pre", preprocessor), ("model", GradientBoostingRegressor(n_estimators=100, random_state=SEED))]),
}

# Treinar e avaliar cada modelo com validação cruzada
resultados = {}
for nome, pipeline in modelos.items():
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5,
                                scoring="neg_mean_absolute_error", n_jobs=-1)
    mae_cv = -cv_scores.mean()
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    resultados[nome] = {
        "MAE_CV": mae_cv,
        "MAE":    mean_absolute_error(y_test, y_pred),
        "RMSE":   np.sqrt(mean_squared_error(y_test, y_pred)),
        "MAPE":   mean_absolute_percentage_error(y_test, y_pred) * 100,
        "R2":     r2_score(y_test, y_pred),
    }
    print(f"  [{nome:22s}] MAE_CV={mae_cv:.4f} | R²={resultados[nome]['R2']:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 6 — AVALIAÇÃO E COMPARAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/8] Resultados completos no conjunto de teste:")
df_resultados = pd.DataFrame(resultados).T.round(4)
print(df_resultados.to_string())

melhor_modelo_nome = df_resultados["R2"].idxmax()
print(f"\n  ✓ Melhor modelo: {melhor_modelo_nome} (R² = {df_resultados.loc[melhor_modelo_nome, 'R2']:.4f})")

# Plot comparativo
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Comparação de Modelos de Regressão", fontsize=14, fontweight="bold")

nomes = list(df_resultados.index)
r2_vals = df_resultados["R2"].values
mae_vals = df_resultados["MAE"].values
cores = ["#4CAF50" if n == melhor_modelo_nome else "#90A4AE" for n in nomes]

axes[0].barh(nomes, r2_vals, color=cores, edgecolor="white")
axes[0].set_title("R² Score (maior é melhor)")
axes[0].set_xlim(0, 1)
axes[0].axvline(0.8, color="red", linestyle="--", alpha=0.5, label="R²=0.8")
axes[0].legend()

axes[1].barh(nomes, mae_vals, color=cores, edgecolor="white")
axes[1].set_title("MAE ($100k) — menor é melhor")

plt.tight_layout()
plt.savefig("regressao_comparacao.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: regressao_comparacao.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 7 — OTIMIZAÇÃO DE HIPERPARÂMETROS (GridSearchCV)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7/8] Otimizando hiperparâmetros do melhor modelo (Gradient Boosting)...")

pipeline_gb = Pipeline([
    ("pre", preprocessor),
    ("model", GradientBoostingRegressor(random_state=SEED))
])

param_grid = {
    "model__n_estimators":   [100, 200],
    "model__max_depth":      [3, 5],
    "model__learning_rate":  [0.05, 0.1],
    "model__subsample":      [0.8, 1.0],
}

grid_search = GridSearchCV(
    pipeline_gb, param_grid, cv=3,
    scoring="neg_mean_absolute_error",
    n_jobs=-1, verbose=0
)
grid_search.fit(X_train, y_train)

melhor_pipeline = grid_search.best_estimator_
y_pred_otimizado = melhor_pipeline.predict(X_test)

print(f"  Melhores parâmetros: {grid_search.best_params_}")
print(f"  MAE otimizado:  {mean_absolute_error(y_test, y_pred_otimizado):.4f}")
print(f"  RMSE otimizado: {np.sqrt(mean_squared_error(y_test, y_pred_otimizado)):.4f}")
print(f"  R² otimizado:   {r2_score(y_test, y_pred_otimizado):.4f}")

# Plot: predito vs real
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Modelo Otimizado — Gradient Boosting", fontsize=14, fontweight="bold")

axes[0].scatter(y_test, y_pred_otimizado, alpha=0.3, s=10, color="#2196F3")
lim = [y_test.min(), y_test.max()]
axes[0].plot(lim, lim, "r--", linewidth=1.5, label="Perfeito")
axes[0].set_xlabel("Valor Real ($100k)")
axes[0].set_ylabel("Valor Predito ($100k)")
axes[0].set_title("Real vs Predito")
axes[0].legend()

residuos = y_test - y_pred_otimizado
axes[1].scatter(y_pred_otimizado, residuos, alpha=0.3, s=10, color="#FF5722")
axes[1].axhline(0, color="black", linewidth=1.5, linestyle="--")
axes[1].set_xlabel("Valor Predito")
axes[1].set_ylabel("Resíduo")
axes[1].set_title("Análise de Resíduos")

plt.tight_layout()
plt.savefig("regressao_resultado_final.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: regressao_resultado_final.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 8 — SERIALIZAÇÃO (PKL) E INFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[8/8] Salvando modelo e realizando inferência...")

# Salvar o pipeline completo (inclui pré-processamento + modelo)
joblib.dump(melhor_pipeline, MODEL_PATH)
print(f"  Modelo salvo em: {MODEL_PATH}")

# ── Carregar o modelo do disco (simula deploy real) ──────────────────────────
modelo_carregado = joblib.load(MODEL_PATH)
print(f"  Modelo carregado do arquivo pkl com sucesso.")

# ── Simular novos dados para inferência ─────────────────────────────────────
novos_imoveis = pd.DataFrame({
    "MedInc":     [8.5,  3.2,  5.0],   # renda mediana
    "HouseAge":   [15,   40,   25],     # idade da casa
    "AveRooms":   [6.5,  4.0,  5.5],   # média de cômodos
    "AveBedrms":  [1.1,  1.2,  1.05],  # média de quartos
    "Population": [800,  1200, 600],    # população do bloco
    "AveOccup":   [2.8,  3.5,  2.5],   # média de moradores
    "Latitude":   [37.8, 34.0, 36.5],
    "Longitude":  [-122.3, -118.2, -120.1],
    # features derivadas
    "rooms_per_household":      [6.5/2.8,  4.0/3.5,  5.5/2.5],
    "bedrooms_ratio":           [1.1/6.5,  1.2/4.0,  1.05/5.5],
    "population_per_household": [800/15,   1200/40,  600/25],
})

previsoes = modelo_carregado.predict(novos_imoveis)

print("\n  ┌─────────────────────────────────────────────┐")
print("  │         INFERÊNCIA — NOVOS IMÓVEIS          │")
print("  ├──────────┬──────────┬──────────┬────────────┤")
print("  │ Imóvel   │ Renda    │ Idade    │ Previsão   │")
print("  ├──────────┼──────────┼──────────┼────────────┤")
for i, (_, row) in enumerate(novos_imoveis.iterrows()):
    print(f"  │ Imóvel {i+1} │  {row['MedInc']:.1f}k    │  {int(row['HouseAge'])} anos  │  ${previsoes[i]*100_000:,.0f}  │")
print("  └──────────┴──────────┴──────────┴────────────┘")

print("\n" + "=" * 70)
print("  REGRESSÃO CONCLUÍDA COM SUCESSO")
print("=" * 70)
