"""
================================================================================
MACHINE LEARNING — CLUSTERING (APRENDIZADO NÃO SUPERVISIONADO)
Problema: Segmentação de Clientes (RFM — Recency, Frequency, Monetary)
================================================================================

ETAPAS COBERTAS:
  1. Geração e entendimento dos dados (RFM sintético)
  2. Análise exploratória (EDA)
  3. Pré-processamento (escalonamento, tratamento de outliers)
  4. Determinação do número ideal de clusters
  5. Treinamento: K-Means, DBSCAN, Agglomerative Clustering
  6. Avaliação dos clusters (Silhouette, Davies-Bouldin, Calinski-Harabasz)
  7. Interpretação e perfilamento dos segmentos
  8. Serialização (pkl) e inferência (classificar novos clientes)

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

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import (
    silhouette_score, davies_bouldin_score, calinski_harabasz_score
)
from sklearn.pipeline import Pipeline
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.stats import zscore

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
MODEL_PATH = Path("modelo_clustering.pkl")
np.random.seed(SEED)

print("=" * 70)
print("  CLUSTERING — SEGMENTAÇÃO DE CLIENTES (RFM)")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 1 — GERAÇÃO DE DADOS SINTÉTICOS (RFM)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/8] Gerando dados RFM sintéticos...")

n_clientes = 1_000

# Simular 4 segmentos distintos de clientes
segmentos = {
    "Campeões":          {"n": 200, "recency": (5, 3),   "frequency": (25, 8),  "monetary": (1500, 400)},
    "Leais":             {"n": 250, "recency": (25, 12),  "frequency": (15, 5),  "monetary": (800, 200)},
    "Em Risco":          {"n": 300, "recency": (120, 40), "frequency": (6, 3),   "monetary": (400, 150)},
    "Clientes Inativos": {"n": 250, "recency": (280, 60), "frequency": (2, 1),   "monetary": (150, 80)},
}

dfs = []
for seg_nome, params in segmentos.items():
    df_seg = pd.DataFrame({
        "recency":   np.random.normal(params["recency"][0],   params["recency"][1],   params["n"]).clip(1, 365),
        "frequency": np.random.normal(params["frequency"][0], params["frequency"][1], params["n"]).clip(1, 50),
        "monetary":  np.random.normal(params["monetary"][0],  params["monetary"][1],  params["n"]).clip(10, 5000),
        "segmento_real": seg_nome
    })
    dfs.append(df_seg)

df = pd.concat(dfs, ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)
df["cliente_id"] = [f"CLI{str(i).zfill(5)}" for i in range(len(df))]

print(f"  Clientes gerados: {len(df)}")
print(f"  Features RFM: recency (dias), frequency (compras), monetary (R$)")
print(f"\n  Estatísticas:\n{df[['recency','frequency','monetary']].describe().round(1).to_string()}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 2 — ANÁLISE EXPLORATÓRIA (EDA)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/8] Análise Exploratória...")

features = ["recency", "frequency", "monetary"]
X_raw = df[features].copy()

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("EDA — Análise RFM dos Clientes", fontsize=14, fontweight="bold")

# Distribuições
for i, feat in enumerate(features):
    axes[0, i].hist(X_raw[feat], bins=40, color="#42A5F5", edgecolor="white", alpha=0.8)
    axes[0, i].set_title(f"Distribuição: {feat}")
    axes[0, i].set_xlabel(feat)
    axes[0, i].set_ylabel("Clientes")

# Scatter plots entre pares de features
pares = [("recency", "frequency"), ("recency", "monetary"), ("frequency", "monetary")]
cores_seg = {"Campeões": "#4CAF50", "Leais": "#2196F3", "Em Risco": "#FF9800", "Clientes Inativos": "#F44336"}
for j, (f1, f2) in enumerate(pares):
    for seg, cor in cores_seg.items():
        mask = df["segmento_real"] == seg
        axes[1, j].scatter(df.loc[mask, f1], df.loc[mask, f2],
                           c=cor, alpha=0.3, s=10, label=seg)
    axes[1, j].set_xlabel(f1)
    axes[1, j].set_ylabel(f2)
    axes[1, j].set_title(f"{f1} vs {f2}")
    if j == 2:
        axes[1, j].legend(fontsize=7, loc="upper right")

plt.tight_layout()
plt.savefig("clustering_eda.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: clustering_eda.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 3 — PRÉ-PROCESSAMENTO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/8] Pré-processamento...")

# Log-transform para reduzir assimetria em monetary e frequency
X_log = X_raw.copy()
X_log["frequency"] = np.log1p(X_log["frequency"])
X_log["monetary"]  = np.log1p(X_log["monetary"])

# RobustScaler: robusto a outliers
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_log)

print(f"  Transformações aplicadas: log1p em frequency e monetary")
print(f"  Escalonamento: RobustScaler (robusto a outliers)")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 4 — DETERMINAÇÃO DO NÚMERO DE CLUSTERS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/8] Determinando número ideal de clusters...")

inercias, silhouettes, db_scores = [], [], []
k_range = range(2, 9)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    inercias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))
    db_scores.append(davies_bouldin_score(X_scaled, labels))

# Plot Elbow + Silhouette
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Determinação do Número Ideal de Clusters", fontsize=14, fontweight="bold")

axes[0].plot(k_range, inercias, "o-", color="#2196F3", linewidth=2)
axes[0].set_title("Método do Cotovelo (Inércia)")
axes[0].set_xlabel("k clusters")
axes[0].set_ylabel("Inércia")
axes[0].axvline(4, color="red", linestyle="--", alpha=0.6, label="k=4")
axes[0].legend()

axes[1].plot(k_range, silhouettes, "o-", color="#4CAF50", linewidth=2)
axes[1].set_title("Silhouette Score (maior = melhor)")
axes[1].set_xlabel("k clusters")
axes[1].set_ylabel("Silhouette")
axes[1].axvline(4, color="red", linestyle="--", alpha=0.6, label="k=4")
axes[1].legend()

axes[2].plot(k_range, db_scores, "o-", color="#FF5722", linewidth=2)
axes[2].set_title("Davies-Bouldin Score (menor = melhor)")
axes[2].set_xlabel("k clusters")
axes[2].set_ylabel("DB Score")
axes[2].axvline(4, color="red", linestyle="--", alpha=0.6, label="k=4")
axes[2].legend()

plt.tight_layout()
plt.savefig("clustering_k_ideal.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: clustering_k_ideal.png")
print(f"  K escolhido: 4 (melhor Silhouette: {max(silhouettes):.4f})")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 5 — TREINAMENTO DE ALGORITMOS DE CLUSTERING
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/8] Treinando algoritmos de clustering...")

K_FINAL = 4

algoritmos = {
    "K-Means":          KMeans(n_clusters=K_FINAL, random_state=SEED, n_init=10),
    "Agglomerative":    AgglomerativeClustering(n_clusters=K_FINAL, linkage="ward"),
    "DBSCAN":           DBSCAN(eps=0.6, min_samples=10),
}

resultados_cluster = {}
for nome, modelo in algoritmos.items():
    labels = modelo.fit_predict(X_scaled)
    n_clusters_encontrados = len(set(labels)) - (1 if -1 in labels else 0)
    n_ruido = (labels == -1).sum()

    if n_clusters_encontrados >= 2:
        mask_valido = labels != -1
        sil = silhouette_score(X_scaled[mask_valido], labels[mask_valido]) if mask_valido.sum() > 1 else 0
        db  = davies_bouldin_score(X_scaled[mask_valido], labels[mask_valido]) if mask_valido.sum() > 1 else 999
        ch  = calinski_harabasz_score(X_scaled[mask_valido], labels[mask_valido]) if mask_valido.sum() > 1 else 0
    else:
        sil, db, ch = 0, 999, 0

    resultados_cluster[nome] = {
        "K encontrado": n_clusters_encontrados,
        "Ruído (DBSCAN)": n_ruido,
        "Silhouette": round(sil, 4),
        "Davies-Bouldin": round(db, 4),
        "Calinski-Harabasz": round(ch, 1),
    }
    print(f"  [{nome:18s}] Clusters={n_clusters_encontrados} | Silhouette={sil:.4f} | DB={db:.4f}")

print("\n  Tabela comparativa:")
print(pd.DataFrame(resultados_cluster).T.to_string())

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 6 — MODELO FINAL: K-MEANS + PERFILAMENTO
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/8] Perfilando segmentos (K-Means final)...")

kmeans_final = KMeans(n_clusters=K_FINAL, random_state=SEED, n_init=10)
df["cluster"] = kmeans_final.fit_predict(X_scaled)

# Perfil médio por cluster
perfil = df.groupby("cluster")[features].mean().round(1)
perfil["tamanho"]   = df.groupby("cluster").size()
perfil["% total"]   = (perfil["tamanho"] / len(df) * 100).round(1)

# Nomear clusters automaticamente com base nas métricas RFM
def nomear_cluster(row):
    if row["recency"] < 30 and row["frequency"] > 15:
        return "🏆 Campeões"
    elif row["recency"] < 60 and row["frequency"] > 10:
        return "⭐ Clientes Leais"
    elif row["recency"] > 150:
        return "💤 Inativos"
    else:
        return "⚠️ Em Risco"

perfil["segmento"] = perfil.apply(nomear_cluster, axis=1)
print(f"\n  Perfil dos Clusters:")
print(perfil.to_string())

# PCA para visualização 2D
pca = PCA(n_components=2, random_state=SEED)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Segmentação de Clientes — K-Means (k=4)", fontsize=14, fontweight="bold")

cores_cluster = {0: "#4CAF50", 1: "#2196F3", 2: "#FF9800", 3: "#F44336"}

for c in range(K_FINAL):
    mask = df["cluster"] == c
    label = perfil.loc[c, "segmento"] if c in perfil.index else f"Cluster {c}"
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1],
                    c=cores_cluster[c], alpha=0.4, s=15, label=label)
axes[0].set_title("Clusters — PCA 2D")
axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
axes[0].legend(fontsize=8)

# Radar / bar chart dos perfis
segmentos_nomes = [perfil.loc[c, "segmento"] for c in range(K_FINAL)]
tamanhos = [perfil.loc[c, "tamanho"] for c in range(K_FINAL)]
axes[1].bar(segmentos_nomes, tamanhos,
            color=[cores_cluster[c] for c in range(K_FINAL)], edgecolor="white")
axes[1].set_title("Tamanho dos Segmentos")
axes[1].set_ylabel("Nº de Clientes")
axes[1].tick_params(axis="x", rotation=20)
for i, v in enumerate(tamanhos):
    axes[1].text(i, v + 5, str(v), ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("clustering_resultado.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: clustering_resultado.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 7 — DENDROGRAMA (AGGLOMERATIVE)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7/8] Gerando dendrograma hierárquico...")

amostra_idx = np.random.choice(len(X_scaled), size=100, replace=False)
Z = linkage(X_scaled[amostra_idx], method="ward")

fig, ax = plt.subplots(figsize=(14, 5))
dendrogram(Z, ax=ax, truncate_mode="lastp", p=20,
           leaf_rotation=45, leaf_font_size=9,
           color_threshold=Z[-4, 2])
ax.set_title("Dendrograma Hierárquico (Ward Linkage) — Amostra 100 clientes")
ax.set_ylabel("Distância")
ax.axhline(y=Z[-4, 2], color="red", linestyle="--", alpha=0.7, label="Corte k=4")
ax.legend()
plt.tight_layout()
plt.savefig("clustering_dendrograma.png", dpi=120, bbox_inches="tight")
plt.close()
print("  Gráfico salvo: clustering_dendrograma.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 8 — SERIALIZAÇÃO (PKL) E INFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[8/8] Salvando modelo e classificando novos clientes...")

# Salvar o pipeline completo: scaler + kmeans
pipeline_clustering = {
    "scaler":  scaler,
    "kmeans":  kmeans_final,
    "perfil":  perfil,
    "log_transform_cols": ["frequency", "monetary"],
    "features": features
}
joblib.dump(pipeline_clustering, MODEL_PATH)
print(f"  Modelo salvo em: {MODEL_PATH}")

# ── Inferência com novos clientes ────────────────────────────────────────────
artefatos = joblib.load(MODEL_PATH)
_scaler   = artefatos["scaler"]
_kmeans   = artefatos["kmeans"]
_perfil   = artefatos["perfil"]
_log_cols = artefatos["log_transform_cols"]
_feats    = artefatos["features"]

novos_clientes = pd.DataFrame({
    "recency":   [3,   350,  45,   180],
    "frequency": [30,  1,    12,   5],
    "monetary":  [2000, 50,  700,  200],
})

# Aplicar mesmas transformações
X_novo = novos_clientes[_feats].copy()
for col in _log_cols:
    X_novo[col] = np.log1p(X_novo[col])
X_novo_scaled = _scaler.transform(X_novo)
clusters_preditos = _kmeans.predict(X_novo_scaled)

print("\n  ┌────────────┬──────────┬───────────┬──────────┬──────────────────────┐")
print("  │ Cliente    │ Recency  │ Frequency │ Monetary │ Segmento             │")
print("  ├────────────┼──────────┼───────────┼──────────┼──────────────────────┤")
for i, row in novos_clientes.iterrows():
    c = clusters_preditos[i]
    seg = _perfil.loc[c, "segmento"] if c in _perfil.index else f"Cluster {c}"
    print(f"  │ Novo {i+1}     │ {int(row['recency']):6d}d  │ {int(row['frequency']):5d}x    │ R${row['monetary']:5.0f}  │ {seg:20s} │")
print("  └────────────┴──────────┴───────────┴──────────┴──────────────────────┘")

print("\n" + "=" * 70)
print("  CLUSTERING CONCLUÍDO COM SUCESSO")
print("=" * 70)
