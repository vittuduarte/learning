"""
================================================================================
MACHINE LEARNING — VISÃO COMPUTACIONAL
Problema: Classificação de Dígitos Manuscritos (MNIST / Digits Dataset)
================================================================================

ETAPAS COBERTAS:
  1. Carregamento e entendimento das imagens
  2. Análise exploratória visual (EDA)
  3. Pré-processamento de imagens
  4. Extração de features (HOG, PCA, pixel flattening)
  5. Treinamento de classificadores para visão
  6. Avaliação completa (confusion matrix, métricas por classe)
  7. Otimização de hiperparâmetros
  8. Serialização (pkl) e inferência em novas imagens

Bibliotecas: scikit-learn, scikit-image, pandas, numpy, matplotlib, joblib
================================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import joblib
from pathlib import Path

from sklearn.datasets import load_digits
from sklearn.model_selection import (
    train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
)
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    f1_score, ConfusionMatrixDisplay
)
from skimage.feature import hog
from skimage.transform import resize as sk_resize

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
MODEL_PATH = Path("modelo_visao_computacional.pkl")
np.random.seed(SEED)

print("=" * 70)
print("  VISÃO COMPUTACIONAL — CLASSIFICAÇÃO DE DÍGITOS MANUSCRITOS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 1 — CARREGAMENTO DAS IMAGENS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/8] Carregando dataset de dígitos (sklearn Digits)...")

digits = load_digits()
X_imagens = digits.images   # shape: (1797, 8, 8) — imagens 8x8 pixels
y = digits.target           # labels: 0-9
X_flat = digits.data        # shape: (1797, 64) — pixels achatados

print(f"  Total de imagens: {len(X_imagens)}")
print(f"  Resolução das imagens: {X_imagens.shape[1]}x{X_imagens.shape[2]} pixels")
print(f"  Classes (dígitos): {sorted(set(y))}")
print(f"  Distribuição:\n{pd.Series(y).value_counts().sort_index().rename('contagem').to_string()}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 2 — ANÁLISE EXPLORATÓRIA VISUAL (EDA)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/8] Análise Exploratória Visual...")

fig = plt.figure(figsize=(16, 10))
fig.suptitle("EDA — Dataset de Dígitos Manuscritos", fontsize=14, fontweight="bold")
gs = gridspec.GridSpec(3, 5, figure=fig, hspace=0.4, wspace=0.3)

# Amostras de cada dígito (0–9)
ax_titulo = fig.add_subplot(gs[0, :])
ax_titulo.axis("off")
ax_titulo.text(0.5, 0.5, "Amostras por Dígito (0–9)", ha="center", va="center",
               fontsize=12, fontweight="bold")

for digito in range(10):
    idx = np.where(y == digito)[0][0]
    row, col = divmod(digito, 5)
    ax = fig.add_subplot(gs[row + 1, col])
    ax.imshow(X_imagens[idx], cmap="gray_r", interpolation="nearest")
    ax.set_title(f"Dígito: {digito}", fontsize=9)
    ax.axis("off")

plt.savefig("visao_eda_amostras.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: visao_eda_amostras.png")

# Intensidade média por dígito (heatmap)
fig, axes = plt.subplots(2, 5, figsize=(16, 7))
fig.suptitle("Média de Pixel por Dígito (8x8)", fontsize=14, fontweight="bold")
for digito in range(10):
    row, col = divmod(digito, 5)
    media_img = X_imagens[y == digito].mean(axis=0)
    im = axes[row, col].imshow(media_img, cmap="hot", interpolation="nearest")
    axes[row, col].set_title(f"Dígito {digito}")
    axes[row, col].axis("off")
    plt.colorbar(im, ax=axes[row, col], fraction=0.04)
plt.tight_layout()
plt.savefig("visao_eda_media_pixels.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: visao_eda_media_pixels.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 3 — PRÉ-PROCESSAMENTO DE IMAGENS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/8] Pré-processamento das imagens...")

# Normalizar pixels para [0, 1]
X_normalizado = X_flat / 16.0  # valores originais: 0-16
print(f"  Normalização: pixels divididos por 16 → range [0.0, 1.0]")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 4 — EXTRAÇÃO DE FEATURES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/8] Extração de Features...")

# ── Estratégia 1: Pixels brutos achatados (baseline) ─────────────────────────
X_pixels = X_normalizado.copy()
print(f"  [Pixels brutos] Shape: {X_pixels.shape}")

# ── Estratégia 2: HOG (Histogram of Oriented Gradients) ─────────────────────
# HOG extrai bordas e texturas — muito usado em visão clássica
def extrair_hog(imagens):
    features = []
    for img in imagens:
        img_resized = sk_resize(img, (16, 16), anti_aliasing=True)
        feat = hog(img_resized, orientations=8, pixels_per_cell=(4, 4),
                   cells_per_block=(2, 2), feature_vector=True)
        features.append(feat)
    return np.array(features)

X_hog = extrair_hog(X_imagens)
print(f"  [HOG features]  Shape: {X_hog.shape}")

# ── Estratégia 3: PCA sobre pixels (redução dimensional) ─────────────────────
pca_viz = PCA(n_components=0.95, random_state=SEED)  # manter 95% da variância
X_pca_viz = pca_viz.fit_transform(X_pixels)
print(f"  [PCA 95% var]   Shape: {X_pca_viz.shape} (de {X_pixels.shape[1]} → {X_pca_viz.shape[1]} componentes)")

# Visualizar PCA 2D
pca_2d = PCA(n_components=2, random_state=SEED)
X_2d = pca_2d.fit_transform(X_pixels)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Redução Dimensional — Espaço de Features", fontsize=14, fontweight="bold")

scatter = axes[0].scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap="tab10", s=8, alpha=0.6)
plt.colorbar(scatter, ax=axes[0], label="Dígito")
axes[0].set_title(f"PCA 2D (var={pca_2d.explained_variance_ratio_.sum()*100:.1f}%)")
axes[0].set_xlabel("PC1")
axes[0].set_ylabel("PC2")

# Variância explicada acumulada
pca_full = PCA(random_state=SEED)
pca_full.fit(X_pixels)
var_acum = np.cumsum(pca_full.explained_variance_ratio_)
axes[1].plot(var_acum, color="#2196F3", linewidth=2)
axes[1].axhline(0.95, color="red", linestyle="--", label="95% variância")
axes[1].axvline(np.argmax(var_acum >= 0.95), color="orange", linestyle="--",
                label=f"{np.argmax(var_acum >= 0.95)} componentes")
axes[1].set_title("Variância Explicada — PCA")
axes[1].set_xlabel("Número de Componentes")
axes[1].set_ylabel("Variância Acumulada")
axes[1].legend()
axes[1].set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig("visao_features.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: visao_features.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 5 — TREINAMENTO DE CLASSIFICADORES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/8] Dividindo e treinando classificadores...")

X_train_p, X_test_p, y_train, y_test = train_test_split(
    X_pixels, y, test_size=0.2, random_state=SEED, stratify=y
)
X_train_h, X_test_h, _, _ = train_test_split(
    X_hog, y, test_size=0.2, random_state=SEED, stratify=y
)
print(f"  Treino: {len(y_train)} | Teste: {len(y_test)}")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

# Modelos com features de pixels
modelos_pixels = {
    "KNN (pixels)":       Pipeline([("sc", StandardScaler()), ("m", KNeighborsClassifier(n_neighbors=5))]),
    "SVM RBF (pixels)":   Pipeline([("sc", StandardScaler()), ("m", SVC(kernel="rbf", C=10, gamma="scale", random_state=SEED))]),
    "RF (pixels)":        Pipeline([("sc", StandardScaler()), ("m", RandomForestClassifier(n_estimators=200, random_state=SEED))]),
    "LR + PCA (pixels)":  Pipeline([("sc", StandardScaler()), ("pca", PCA(n_components=30)), ("m", LogisticRegression(max_iter=1000, random_state=SEED))]),
}

# Modelos com HOG
modelos_hog = {
    "SVM RBF (HOG)":  Pipeline([("sc", StandardScaler()), ("m", SVC(kernel="rbf", C=10, random_state=SEED))]),
    "RF (HOG)":       Pipeline([("sc", StandardScaler()), ("m", RandomForestClassifier(n_estimators=200, random_state=SEED))]),
}

resultados = {}
for nome, pipeline in modelos_pixels.items():
    cv_sc = cross_val_score(pipeline, X_train_p, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
    pipeline.fit(X_train_p, y_train)
    acc = accuracy_score(y_test, pipeline.predict(X_test_p))
    resultados[nome] = {"ACC_CV": cv_sc.mean(), "ACC_Test": acc}
    print(f"  [{nome:22s}] CV_Acc={cv_sc.mean():.4f} | Test_Acc={acc:.4f}")

for nome, pipeline in modelos_hog.items():
    cv_sc = cross_val_score(pipeline, X_train_h, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
    pipeline.fit(X_train_h, y_train)
    acc = accuracy_score(y_test, pipeline.predict(X_test_h))
    resultados[nome] = {"ACC_CV": cv_sc.mean(), "ACC_Test": acc}
    print(f"  [{nome:22s}] CV_Acc={cv_sc.mean():.4f} | Test_Acc={acc:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 6 — AVALIAÇÃO COMPLETA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/8] Avaliação completa...")

df_resultados = pd.DataFrame(resultados).T.round(4)
print(df_resultados.to_string())

# SVM com pixels é geralmente o melhor neste dataset
melhor_nome  = "SVM RBF (pixels)"
melhor_model = modelos_pixels[melhor_nome]
y_pred_test  = melhor_model.predict(X_test_p)

print(f"\n  ✓ Melhor modelo: {melhor_nome} (Acc={df_resultados.loc[melhor_nome,'ACC_Test']:.4f})")
print(f"\n  Relatório por classe:")
print(classification_report(y_test, y_pred_test, target_names=[str(d) for d in range(10)]))

# Plot: matriz de confusão + exemplos de erros
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(f"Avaliação — {melhor_nome}", fontsize=14, fontweight="bold")

cm = confusion_matrix(y_test, y_pred_test)
ConfusionMatrixDisplay(cm, display_labels=list(range(10))).plot(
    ax=axes[0], cmap="Blues", colorbar=False, values_format="d"
)
axes[0].set_title("Matriz de Confusão")

# Accuracy por dígito
acc_por_digito = cm.diagonal() / cm.sum(axis=1)
axes[1].bar(range(10), acc_por_digito, color="#4CAF50", edgecolor="white")
axes[1].set_title("Accuracy por Dígito")
axes[1].set_xlabel("Dígito")
axes[1].set_ylabel("Accuracy")
axes[1].set_xticks(range(10))
axes[1].axhline(acc_por_digito.mean(), color="red", linestyle="--",
                label=f"Média: {acc_por_digito.mean():.3f}")
axes[1].legend()
axes[1].set_ylim(0.85, 1.01)

plt.tight_layout()
plt.savefig("visao_avaliacao.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: visao_avaliacao.png")

# Mostrar exemplos de erros
erros_idx = np.where(y_pred_test != y_test)[0]
print(f"\n  Total de erros: {len(erros_idx)} de {len(y_test)} ({len(erros_idx)/len(y_test)*100:.1f}%)")

if len(erros_idx) > 0:
    fig, axes = plt.subplots(2, min(8, len(erros_idx)), figsize=(14, 4))
    fig.suptitle("Exemplos de Classificações Incorretas", fontsize=12, fontweight="bold")
    n_mostrar = min(8, len(erros_idx))
    for i in range(n_mostrar):
        idx = erros_idx[i]
        img = X_test_p[idx].reshape(8, 8)
        axes[0, i].imshow(img, cmap="gray_r")
        axes[0, i].set_title(f"Real: {y_test[idx]}", fontsize=8, color="green")
        axes[0, i].axis("off")
        axes[1, i].imshow(img, cmap="Reds")
        axes[1, i].set_title(f"Pred: {y_pred_test[idx]}", fontsize=8, color="red")
        axes[1, i].axis("off")
    plt.tight_layout()
    plt.savefig("visao_erros.png", dpi=120, bbox_inches="tight")
    plt.close()
    print("  Gráfico salvo: visao_erros.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 7 — OTIMIZAÇÃO DE HIPERPARÂMETROS (SVM)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7/8] Otimizando SVM com GridSearchCV...")

pipeline_svm = Pipeline([
    ("scaler", StandardScaler()),
    ("pca",    PCA(n_components=30, random_state=SEED)),
    ("svm",    SVC(kernel="rbf", probability=True, random_state=SEED))
])

param_grid = {
    "svm__C":     [1, 10, 100],
    "svm__gamma": ["scale", "auto", 0.001],
}

grid_svm = GridSearchCV(
    pipeline_svm, param_grid, cv=3,
    scoring="accuracy", n_jobs=-1, verbose=0
)
grid_svm.fit(X_train_p, y_train)

modelo_final = grid_svm.best_estimator_
y_pred_final = modelo_final.predict(X_test_p)

print(f"  Melhores parâmetros: {grid_svm.best_params_}")
print(f"  Accuracy final: {accuracy_score(y_test, y_pred_final):.4f}")
print(f"  F1 (macro):     {f1_score(y_test, y_pred_final, average='macro'):.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 8 — SERIALIZAÇÃO (PKL) E INFERÊNCIA EM NOVAS IMAGENS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[8/8] Salvando modelo e realizando inferência...")

artefatos = {
    "pipeline":   modelo_final,
    "classes":    list(range(10)),
    "input_shape": (8, 8),
    "n_pixels":   64,
    "normalize_factor": 16.0,
}
joblib.dump(artefatos, MODEL_PATH)
print(f"  Modelo salvo em: {MODEL_PATH}")

# ── Carregar modelo e inferir novas imagens ───────────────────────────────────
artefatos_carregados = joblib.load(MODEL_PATH)
_pipeline = artefatos_carregados["pipeline"]
_fator    = artefatos_carregados["normalize_factor"]
print(f"  Modelo carregado com sucesso.")

# Usar 10 imagens do conjunto de teste como "novas imagens"
n_novas = 10
idx_novos = np.random.choice(len(X_test_p), n_novas, replace=False)
X_novas       = X_test_p[idx_novos]           # já normalizado
y_real_novas  = y_test[idx_novos]

# Predição e probabilidades
previsoes_novas   = _pipeline.predict(X_novas)
probs_novas       = _pipeline.predict_proba(X_novas)

print(f"\n  Inferência em {n_novas} novas imagens:")
print("  ┌──────┬────────┬──────────┬─────────────┐")
print("  │ #    │ Real   │ Predição │ Confiança   │")
print("  ├──────┼────────┼──────────┼─────────────┤")
for i in range(n_novas):
    real = y_real_novas[i]
    pred = previsoes_novas[i]
    confianca = probs_novas[i].max() * 100
    ok = "✓" if real == pred else "✗"
    print(f"  │ {i+1:4d} │  {real}  {ok}  │    {pred}     │   {confianca:5.1f}%   │")
print("  └──────┴────────┴──────────┴─────────────┘")

# Visualização das inferências
fig, axes = plt.subplots(2, 5, figsize=(14, 6))
fig.suptitle("Inferência em Novas Imagens", fontsize=14, fontweight="bold")
for i, ax in enumerate(axes.flat):
    img = X_novas[i].reshape(8, 8)
    pred = previsoes_novas[i]
    real = y_real_novas[i]
    conf = probs_novas[i].max() * 100
    cor = "green" if pred == real else "red"
    ax.imshow(img, cmap="gray_r", interpolation="nearest")
    ax.set_title(f"Pred:{pred} Real:{real}\n{conf:.1f}%", fontsize=8, color=cor)
    ax.axis("off")

plt.tight_layout()
plt.savefig("visao_inferencia.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: visao_inferencia.png")

acuracia_inferencia = (previsoes_novas == y_real_novas).mean() * 100
print(f"\n  Acurácia nas novas imagens: {acuracia_inferencia:.0f}%")

print("\n" + "=" * 70)
print("  VISÃO COMPUTACIONAL CONCLUÍDA COM SUCESSO")
print("=" * 70)
