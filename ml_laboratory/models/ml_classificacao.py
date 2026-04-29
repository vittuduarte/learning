"""
================================================================================
MACHINE LEARNING — CLASSIFICAÇÃO
Problema: Diagnóstico de Câncer de Mama (Breast Cancer Wisconsin)
================================================================================

ETAPAS COBERTAS:
  1. Carregamento e entendimento dos dados
  2. Análise exploratória (EDA)
  3. Pré-processamento
  4. Divisão treino/teste estratificada
  5. Treinamento de múltiplos classificadores
  6. Avaliação com métricas de classificação
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

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import (
    train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    roc_curve, precision_recall_curve, ConfusionMatrixDisplay,
    f1_score, accuracy_score, average_precision_score
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
MODEL_PATH = Path("modelo_classificacao.pkl")
np.random.seed(SEED)

print("=" * 70)
print("  CLASSIFICAÇÃO — DIAGNÓSTICO DE CÂNCER DE MAMA")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 1 — CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/8] Carregando dados...")

cancer = load_breast_cancer(as_frame=True)
df = cancer.frame.copy()
# target: 0 = Maligno, 1 = Benigno
CLASSES = cancer.target_names  # ['malignant', 'benign']

print(f"  Shape: {df.shape}")
print(f"  Classes: {dict(zip([0,1], CLASSES))}")
print(f"  Distribuição:\n{df['target'].value_counts().rename({0: 'Maligno', 1: 'Benigno'}).to_string()}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 2 — ANÁLISE EXPLORATÓRIA (EDA)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/8] Análise Exploratória...")

print(f"  Valores ausentes: {df.isnull().sum().sum()}")
print(f"  Features: {len(cancer.feature_names)}")

# Plot: distribuição do target + box plots das top features
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("EDA — Diagnóstico de Câncer de Mama", fontsize=14, fontweight="bold")

# Distribuição das classes
contagens = df["target"].value_counts()
axes[0].bar(["Maligno", "Benigno"], contagens.values,
            color=["#F44336", "#4CAF50"], edgecolor="white", width=0.5)
axes[0].set_title("Distribuição das Classes")
axes[0].set_ylabel("Amostras")
for i, v in enumerate(contagens.values):
    axes[0].text(i, v + 3, str(v), ha="center", fontweight="bold")

# Box plot das top 4 features mais discriminativas
top_features = ["mean radius", "mean texture", "mean perimeter", "mean area"]
for i, feat in enumerate(top_features[:2]):
    df.boxplot(column=feat, by="target", ax=axes[i+1],
               boxprops=dict(color="#2196F3"),
               medianprops=dict(color="red", linewidth=2))
    axes[i+1].set_title(f"{feat} por Classe")
    axes[i+1].set_xticklabels(["Maligno", "Benigno"])
    axes[i+1].set_xlabel("")
    plt.sca(axes[i+1])
    plt.title(f"{feat} por Classe")

plt.tight_layout()
plt.savefig("classificacao_eda.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: classificacao_eda.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 3 — PRÉ-PROCESSAMENTO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/8] Pré-processamento...")

X = df.drop("target", axis=1)
y = df["target"]

# Pipeline base de pré-processamento
preprocessor = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

print(f"  Features de entrada: {X.shape[1]}")
print(f"  Amostras totais: {X.shape[0]}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 4 — DIVISÃO TREINO/TESTE (ESTRATIFICADA)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/8] Divisão estratificada treino/teste (75%/25%)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)
print(f"  Treino: {X_train.shape[0]} | Teste: {X_test.shape[0]}")
print(f"  Proporção no treino: {y_train.value_counts(normalize=True).round(3).to_dict()}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 5 — TREINAMENTO DE MÚLTIPLOS CLASSIFICADORES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/8] Treinando classificadores...")

classificadores = {
    "Regressão Logística":   Pipeline([("pre", preprocessor), ("model", LogisticRegression(max_iter=1000, random_state=SEED))]),
    "KNN":                   Pipeline([("pre", preprocessor), ("model", KNeighborsClassifier(n_neighbors=7))]),
    "Árvore de Decisão":     Pipeline([("pre", preprocessor), ("model", DecisionTreeClassifier(max_depth=5, random_state=SEED))]),
    "SVM (RBF)":             Pipeline([("pre", preprocessor), ("model", SVC(kernel="rbf", probability=True, random_state=SEED))]),
    "Random Forest":         Pipeline([("pre", preprocessor), ("model", RandomForestClassifier(n_estimators=100, random_state=SEED))]),
    "Gradient Boosting":     Pipeline([("pre", preprocessor), ("model", GradientBoostingClassifier(n_estimators=100, random_state=SEED))]),
}

cv_estratificado = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
resultados = {}

for nome, pipeline in classificadores.items():
    cv_scores = cross_val_score(pipeline, X_train, y_train,
                                cv=cv_estratificado, scoring="roc_auc", n_jobs=-1)
    pipeline.fit(X_train, y_train)
    y_pred      = pipeline.predict(X_test)
    y_pred_prob = pipeline.predict_proba(X_test)[:, 1]

    resultados[nome] = {
        "AUC_CV":   cv_scores.mean(),
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1":       f1_score(y_test, y_pred),
        "ROC-AUC":  roc_auc_score(y_test, y_pred_prob),
        "AP":       average_precision_score(y_test, y_pred_prob),
    }
    print(f"  [{nome:22s}] AUC_CV={cv_scores.mean():.4f} | F1={resultados[nome]['F1']:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 6 — AVALIAÇÃO COMPLETA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/8] Métricas completas no conjunto de teste:")
df_resultados = pd.DataFrame(resultados).T.round(4)
print(df_resultados.to_string())

melhor_nome = df_resultados["ROC-AUC"].idxmax()
melhor_pipeline = classificadores[melhor_nome]
print(f"\n  ✓ Melhor modelo: {melhor_nome} (ROC-AUC = {df_resultados.loc[melhor_nome, 'ROC-AUC']:.4f})")

# Relatório detalhado do melhor modelo
y_pred_melhor = melhor_pipeline.predict(X_test)
print(f"\n  Relatório de Classificação — {melhor_nome}:")
print(classification_report(y_test, y_pred_melhor, target_names=["Maligno", "Benigno"]))

# Plot: curvas ROC + matriz de confusão
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle(f"Avaliação — {melhor_nome}", fontsize=14, fontweight="bold")

# Curvas ROC de todos os modelos
for nome, pipeline in classificadores.items():
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    lw = 2.5 if nome == melhor_nome else 1
    ls = "-" if nome == melhor_nome else "--"
    axes[0].plot(fpr, tpr, linewidth=lw, linestyle=ls, label=f"{nome} (AUC={auc:.3f})")
axes[0].plot([0,1],[0,1], "k--", linewidth=1)
axes[0].set_xlabel("FPR")
axes[0].set_ylabel("TPR")
axes[0].set_title("Curvas ROC")
axes[0].legend(fontsize=7)

# Curva Precision-Recall do melhor modelo
y_prob_melhor = melhor_pipeline.predict_proba(X_test)[:, 1]
prec, rec, _ = precision_recall_curve(y_test, y_prob_melhor)
ap = average_precision_score(y_test, y_prob_melhor)
axes[1].plot(rec, prec, color="#4CAF50", linewidth=2.5, label=f"AP = {ap:.3f}")
axes[1].fill_between(rec, prec, alpha=0.15, color="#4CAF50")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].set_title("Curva Precision-Recall")
axes[1].legend()

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred_melhor)
ConfusionMatrixDisplay(cm, display_labels=["Maligno", "Benigno"]).plot(ax=axes[2], cmap="Blues", colorbar=False)
axes[2].set_title("Matriz de Confusão")

plt.tight_layout()
plt.savefig("classificacao_avaliacao.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: classificacao_avaliacao.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 7 — OTIMIZAÇÃO DE HIPERPARÂMETROS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7/8] Otimizando hiperparâmetros (Random Forest)...")

pipeline_rf = Pipeline([
    ("pre", preprocessor),
    ("model", RandomForestClassifier(random_state=SEED))
])

param_grid = {
    "model__n_estimators": [100, 200],
    "model__max_depth":    [None, 10, 20],
    "model__min_samples_split": [2, 5],
    "model__max_features": ["sqrt", "log2"],
}

grid_search = GridSearchCV(
    pipeline_rf, param_grid, cv=cv_estratificado,
    scoring="roc_auc", n_jobs=-1, verbose=0
)
grid_search.fit(X_train, y_train)

modelo_final = grid_search.best_estimator_
y_pred_final = modelo_final.predict(X_test)
y_prob_final = modelo_final.predict_proba(X_test)[:, 1]

print(f"  Melhores parâmetros: {grid_search.best_params_}")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_final):.4f}")
print(f"  F1-Score: {f1_score(y_test, y_pred_final):.4f}")
print(f"  ROC-AUC:  {roc_auc_score(y_test, y_prob_final):.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 8 — SERIALIZAÇÃO (PKL) E INFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[8/8] Salvando modelo e realizando inferência...")

joblib.dump(modelo_final, MODEL_PATH)
print(f"  Modelo salvo em: {MODEL_PATH}")

# ── Carregar modelo e realizar inferência ────────────────────────────────────
modelo_carregado = joblib.load(MODEL_PATH)
print(f"  Modelo carregado com sucesso.")

# Simular 3 novos pacientes com features reais do dataset
novos_pacientes = pd.DataFrame(
    X_test.iloc[:3].values,
    columns=X.columns
)
diagnosticos_reais = y_test.iloc[:3].values

previsoes        = modelo_carregado.predict(novos_pacientes)
probabilidades   = modelo_carregado.predict_proba(novos_pacientes)

print("\n  ┌───────────┬──────────────┬────────────────┬───────────────────────┐")
print("  │ Paciente  │ Real         │ Predição       │ Probabilidade         │")
print("  ├───────────┼──────────────┼────────────────┼───────────────────────┤")
for i in range(3):
    real = CLASSES[diagnosticos_reais[i]]
    pred = CLASSES[previsoes[i]]
    prob_maligno = probabilidades[i][0] * 100
    prob_benigno = probabilidades[i][1] * 100
    ok = "✓" if diagnosticos_reais[i] == previsoes[i] else "✗"
    print(f"  │ Pac. {i+1} {ok}   │ {real:12s} │ {pred:14s} │ M:{prob_maligno:.1f}% / B:{prob_benigno:.1f}%  │")
print("  └───────────┴──────────────┴────────────────┴───────────────────────┘")

print("\n" + "=" * 70)
print("  CLASSIFICAÇÃO CONCLUÍDA COM SUCESSO")
print("=" * 70)
