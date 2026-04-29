"""
================================================================================
DEEP LEARNING — VISÃO COMPUTACIONAL COM CNN
Problema: Classificação de Imagens — CIFAR-10
          (10 classes: avião, carro, pássaro, gato, cervo,
           cachorro, sapo, cavalo, navio, caminhão)
================================================================================

ETAPAS COBERTAS:
  1.  Carregamento e entendimento do dataset (CIFAR-10)
  2.  Análise exploratória visual (EDA)
  3.  Pré-processamento e Data Augmentation
  4.  Arquitetura CNN Baseline (3 blocos conv do zero)
  5.  Treinamento com callbacks (EarlyStopping, ReduceLROnPlateau,
      ModelCheckpoint, CSVLogger)
  6.  Avaliação: accuracy, curvas loss/accuracy, confusion matrix
  7.  Transfer Learning com MobileNetV2 (2 fases: feature extraction + fine-tuning)
  8.  Comparação Baseline vs Transfer Learning
  9.  Serialização (.keras + .pkl do histórico) e inferência em novas imagens
  10. Grad-CAM: mapa de ativação para explicar o que a CNN "vê"

Frameworks: TensorFlow 2.x / Keras 3, scikit-learn, numpy, matplotlib
================================================================================
"""

from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, CSVLogger
)
from tensorflow.keras import layers, Model, Input
from tensorflow import keras
import tensorflow as tf
from pathlib import Path
import time
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
NUM_CLASSES = 10
BATCH_SIZE = 64
EPOCHS_BASE = 40
EPOCHS_TL = 20

MODEL_BASELINE_PATH = Path("cnn_baseline.keras")
MODEL_TL_PATH = Path("cnn_transfer_learning.keras")
HISTORICO_PATH = Path("cnn_historicos.pkl")

CLASSES = ["avião", "carro", "pássaro", "gato", "cervo",
           "cachorro", "sapo", "cavalo", "navio", "caminhão"]

tf.random.set_seed(SEED)
np.random.seed(SEED)

print("=" * 70)
print("  DEEP LEARNING — CNN — CLASSIFICAÇÃO CIFAR-10")
print(f"  TensorFlow {tf.__version__}  |  Keras {keras.__version__}")
gpus = tf.config.list_physical_devices("GPU")
print(f"  Dispositivo: {'GPU — ' + gpus[0].name if gpus else 'CPU'}")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 1 — CARREGAMENTO DO DATASET
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/10] Carregando CIFAR-10...")

(X_train_raw, y_train_raw), (X_test_raw,
                             y_test_raw) = keras.datasets.cifar10.load_data()
y_train_raw = y_train_raw.flatten()
y_test_raw = y_test_raw.flatten()

print(f"  Treino : {X_train_raw.shape}  dtype={X_train_raw.dtype}")
print(f"  Teste  : {X_test_raw.shape}")
print(f"  Classes: {NUM_CLASSES} → {CLASSES}")
unique, counts = np.unique(y_train_raw, return_counts=True)
print(f"  Distribuição treino: {dict(zip(unique.tolist(), counts.tolist()))}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 2 — ANÁLISE EXPLORATÓRIA VISUAL
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/10] Análise Exploratória Visual...")

# Grid 5 amostras × 10 classes
fig, axes = plt.subplots(NUM_CLASSES, 5, figsize=(10, 22))
fig.suptitle("CIFAR-10 — 5 Amostras por Classe", fontsize=14,
             fontweight="bold", y=1.005)
for cls_idx, cls_nome in enumerate(CLASSES):
    idxs = np.where(y_train_raw == cls_idx)[0][:5]
    for col, img_idx in enumerate(idxs):
        axes[cls_idx, col].imshow(X_train_raw[img_idx])
        axes[cls_idx, col].axis("off")
        if col == 0:
            axes[cls_idx, col].set_ylabel(
                cls_nome, fontsize=9, rotation=90,
                labelpad=40, va="center", fontweight="bold"
            )
plt.tight_layout()
plt.savefig("cnn_eda_amostras.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_eda_amostras.png")

# Distribuição de classes + histograma RGB
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("EDA — Distribuição e Estatísticas de Pixel", fontsize=13,
             fontweight="bold")

contagens = [int(np.sum(y_train_raw == i)) for i in range(NUM_CLASSES)]
cores_bar = plt.cm.tab10(np.linspace(0, 1, NUM_CLASSES))
bars = axes[0].bar(CLASSES, contagens, color=cores_bar, edgecolor="white")
axes[0].set_title("Distribuição das Classes (Treino)")
axes[0].set_ylabel("Amostras")
axes[0].tick_params(axis="x", rotation=35)
for bar, cnt in zip(bars, contagens):
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 20, str(cnt),
                 ha="center", fontsize=8)

for c, cor in enumerate(["red", "green", "blue"]):
    axes[1].hist(
        X_train_raw[:1000, :, :, c].flatten(),
        bins=50, color=cor, alpha=0.5,
        label=f"Canal {cor.upper()}", density=True
    )
axes[1].set_title("Intensidade de Pixels — amostra 1000 imagens")
axes[1].set_xlabel("Valor do Pixel (0–255)")
axes[1].set_ylabel("Densidade")
axes[1].legend()
plt.tight_layout()
plt.savefig("cnn_eda_distribuicao.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_eda_distribuicao.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 3 — PRÉ-PROCESSAMENTO E DATA AUGMENTATION
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/10] Pré-processamento e Data Augmentation...")

# Normalização [0,255] → [0.0,1.0]
X_train = X_train_raw.astype("float32") / 255.0
X_test = X_test_raw.astype("float32") / 255.0

# One-hot encoding
y_train = keras.utils.to_categorical(y_train_raw, NUM_CLASSES)
y_test = keras.utils.to_categorical(y_test_raw,  NUM_CLASSES)

# Split validação (10%)
n_val = int(len(X_train) * 0.1)
X_val,    y_val = X_train[:n_val],  y_train[:n_val]
X_train_, y_train_ = X_train[n_val:],  y_train[n_val:]

print(
    f"  Treino: {X_train_.shape[0]}  |  Val: {X_val.shape[0]}  |  Teste: {X_test.shape[0]}")

# Camada de augmentation (executada inline no grafo)
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomTranslation(0.1, 0.1),
    layers.RandomContrast(0.1),
], name="data_augmentation")

# Visualizar augmentação
fig, axes = plt.subplots(2, 8, figsize=(16, 5))
fig.suptitle("Data Augmentation — Variações da Mesma Imagem", fontsize=13,
             fontweight="bold")
img_ex = X_train_[0:1]
axes[0, 0].imshow(img_ex[0])
axes[0, 0].set_title("Original", fontsize=8)
axes[0, 0].axis("off")
for i in range(1, 16):
    row, col = divmod(i, 8)
    aug = data_augmentation(img_ex, training=True)[0].numpy().clip(0, 1)
    axes[row, col].imshow(aug)
    axes[row, col].set_title(f"Aug {i}", fontsize=8)
    axes[row, col].axis("off")
plt.tight_layout()
plt.savefig("cnn_augmentation.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_augmentation.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 4 — ARQUITETURA CNN BASELINE (do zero)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/10] Construindo CNN Baseline...")


def build_cnn_baseline(input_shape=(32, 32, 3), num_classes=10):
    """
    3 blocos convolucionais progressivos:
      Bloco 1 → Conv(32) × 2 + BN + ReLU + MaxPool + Dropout(0.25)
      Bloco 2 → Conv(64) × 2 + BN + ReLU + MaxPool + Dropout(0.25)
      Bloco 3 → Conv(128)× 2 + BN + ReLU + MaxPool + Dropout(0.25)
      Head    → GlobalAvgPool → Dense(256) + BN + Dropout(0.5) → Softmax
    """
    inp = Input(shape=input_shape)
    x = data_augmentation(inp)

    for filters in [32, 64, 128]:
        x = layers.Conv2D(filters, (3, 3), padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.Conv2D(filters, (3, 3), padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Dropout(0.5)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)

    return Model(inp, out, name="CNN_Baseline")


modelo_baseline = build_cnn_baseline()
modelo_baseline.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy",
             keras.metrics.TopKCategoricalAccuracy(k=3, name="top3_acc")]
)
modelo_baseline.summary()
print(f"\n  Parâmetros totais: {modelo_baseline.count_params():,}")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 5 — TREINAMENTO COM CALLBACKS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/10] Treinando CNN Baseline...")

callbacks_base = [
    EarlyStopping(monitor="val_accuracy", patience=8,
                  restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                      patience=4, min_lr=1e-6, verbose=1),
    ModelCheckpoint(str(MODEL_BASELINE_PATH), monitor="val_accuracy",
                    save_best_only=True, verbose=0),
    CSVLogger("cnn_baseline_log.csv"),
]

t0 = time.time()
hist_baseline = modelo_baseline.fit(
    X_train_, y_train_,
    validation_data=(X_val, y_val),
    epochs=EPOCHS_BASE,
    batch_size=BATCH_SIZE,
    callbacks=callbacks_base,
    verbose=1,
)
print(f"\n  Tempo de treino: {time.time() - t0:.0f}s")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 6 — AVALIAÇÃO DO BASELINE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/10] Avaliando CNN Baseline...")

res_base = modelo_baseline.evaluate(X_test, y_test, verbose=0)
acc_base, top3_base = res_base[1], res_base[2]
print(f"  Loss:      {res_base[0]:.4f}")
print(f"  Accuracy:  {acc_base*100:.2f}%")
print(f"  Top-3 Acc: {top3_base*100:.2f}%")

y_pred_base = np.argmax(modelo_baseline.predict(X_test, verbose=0), axis=1)
y_test_classes = np.argmax(y_test, axis=1)

print(f"\n  Classification Report:")
print(classification_report(y_test_classes, y_pred_base,
                            target_names=CLASSES, digits=4))


def plot_historico(hist_dict, titulo, filename):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(titulo, fontsize=13, fontweight="bold")

    axes[0].plot(hist_dict["loss"],     label="Treino",
                 color="#2196F3", lw=2)
    axes[0].plot(hist_dict["val_loss"], label="Validação",
                 color="#FF5722", lw=2, ls="--")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Época")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(hist_dict["accuracy"],
                 label="Treino",    color="#4CAF50", lw=2)
    axes[1].plot(hist_dict["val_accuracy"], label="Validação",
                 color="#9C27B0", lw=2, ls="--")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Época")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig(filename, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"  Salvo: {filename}")


plot_historico(hist_baseline.history,
               "CNN Baseline — Curvas de Treinamento",
               "cnn_baseline_curvas.png")

fig, ax = plt.subplots(figsize=(11, 9))
cm = confusion_matrix(y_test_classes, y_pred_base)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
            xticklabels=CLASSES, yticklabels=CLASSES, linewidths=0.4)
ax.set_title(f"Confusion Matrix — CNN Baseline  (Acc={acc_base*100:.2f}%)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Predição")
ax.set_ylabel("Real")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig("cnn_baseline_confusion.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_baseline_confusion.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 7 — TRANSFER LEARNING COM MobileNetV2
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7/10] Transfer Learning — MobileNetV2...")


def build_mobilenet_model(input_shape=(32, 32, 3), num_classes=10):
    """
    Pipeline TL:
      1. UpSampling2D 32→96 px (MobileNetV2 requer >= 32; 96 melhora representação)
      2. Data Augmentation
      3. Pré-processamento MobileNetV2 (normalização [-1, 1])
      4. MobileNetV2 backbone (pesos ImageNet, congelado na Fase 1)
      5. GlobalAveragePooling → Dense(256) → Dropout → Softmax
    """
    inp = Input(shape=input_shape)
    x = layers.UpSampling2D(size=(3, 3), interpolation="bilinear")(inp)
    x = data_augmentation(x)
    x = layers.Lambda(
        lambda t: tf.keras.applications.mobilenet_v2.preprocess_input(
            t * 255.0),
        name="mobilenet_preprocess"
    )(x)

    backbone = MobileNetV2(
        input_shape=(96, 96, 3),
        include_top=False,
        weights="imagenet",
    )
    backbone.trainable = False

    x = backbone(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)

    return Model(inp, out, name="MobileNetV2_TL"), backbone


modelo_tl, backbone = build_mobilenet_model()
modelo_tl.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy",
             keras.metrics.TopKCategoricalAccuracy(k=3, name="top3_acc")]
)

# ── Fase 1: treinar apenas a cabeça ──────────────────────────────────────────
print("\n  [Fase 1] Backbone congelado — treinando cabeça...")
n_train_f1 = sum(np.prod(v.shape) for v in modelo_tl.trainable_variables)
print(f"  Parâmetros treináveis: {n_train_f1:,}")

hist_f1 = modelo_tl.fit(
    X_train_, y_train_,
    validation_data=(X_val, y_val),
    epochs=10,
    batch_size=BATCH_SIZE,
    callbacks=[EarlyStopping(monitor="val_accuracy", patience=5,
                             restore_best_weights=True, verbose=1)],
    verbose=1,
)

# ── Fase 2: fine-tuning das últimas 30 camadas ───────────────────────────────
print("\n  [Fase 2] Fine-tuning — últimas 30 camadas do backbone...")
backbone.trainable = True
for layer in backbone.layers[:-30]:
    layer.trainable = False

n_train_f2 = sum(np.prod(v.shape) for v in modelo_tl.trainable_variables)
print(f"  Parâmetros treináveis: {n_train_f2:,}")

modelo_tl.compile(
    optimizer=keras.optimizers.Adam(1e-4),     # LR menor para fine-tuning
    loss="categorical_crossentropy",
    metrics=["accuracy",
             keras.metrics.TopKCategoricalAccuracy(k=3, name="top3_acc")]
)

t0 = time.time()
hist_f2 = modelo_tl.fit(
    X_train_, y_train_,
    validation_data=(X_val, y_val),
    epochs=EPOCHS_TL,
    batch_size=BATCH_SIZE,
    callbacks=[
        EarlyStopping(monitor="val_accuracy", patience=6,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3,
                          patience=3, min_lr=1e-7, verbose=1),
        ModelCheckpoint(str(MODEL_TL_PATH), monitor="val_accuracy",
                        save_best_only=True, verbose=0),
        CSVLogger("cnn_tl_log.csv"),
    ],
    verbose=1,
)
print(f"\n  Tempo fine-tuning: {time.time() - t0:.0f}s")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 8 — COMPARAÇÃO BASELINE vs TRANSFER LEARNING
# ─────────────────────────────────────────────────────────────────────────────
print("\n[8/10] Comparando modelos...")

res_tl = modelo_tl.evaluate(X_test, y_test, verbose=0)
acc_tl, top3_tl = res_tl[1], res_tl[2]
y_pred_tl = np.argmax(modelo_tl.predict(X_test, verbose=0), axis=1)

print(f"\n  ┌──────────────────────────────┬────────────┬────────────┐")
print(f"  │ Modelo                       │ Accuracy   │ Top-3 Acc  │")
print(f"  ├──────────────────────────────┼────────────┼────────────┤")
print(
    f"  │ CNN Baseline (do zero)       │  {acc_base*100:6.2f}%  │  {top3_base*100:6.2f}%  │")
print(
    f"  │ MobileNetV2 (Transfer L.)    │  {acc_tl*100:6.2f}%  │  {top3_tl*100:6.2f}%  │")
print(f"  └──────────────────────────────┴────────────┴────────────┘")
print(f"  Ganho: +{(acc_tl - acc_base)*100:.2f} pp")

# F1 por classe — comparativo
rep_base = classification_report(y_test_classes, y_pred_base,
                                 target_names=CLASSES, output_dict=True)
rep_tl = classification_report(y_test_classes, y_pred_tl,
                               target_names=CLASSES, output_dict=True)
f1_base_cls = [rep_base[c]["f1-score"] for c in CLASSES]
f1_tl_cls = [rep_tl[c]["f1-score"] for c in CLASSES]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("CNN Baseline vs MobileNetV2 Transfer Learning",
             fontsize=14, fontweight="bold")

x = np.arange(len(CLASSES))
w = 0.35
axes[0].bar(x - w/2, f1_base_cls, w, label=f"Baseline ({acc_base*100:.1f}%)",
            color="#2196F3", edgecolor="white")
axes[0].bar(x + w/2, f1_tl_cls,   w, label=f"MobileNetV2 ({acc_tl*100:.1f}%)",
            color="#4CAF50", edgecolor="white")
axes[0].set_xticks(x)
axes[0].set_xticklabels(CLASSES, rotation=35, ha="right")
axes[0].set_ylabel("F1-Score")
axes[0].set_title("F1-Score por Classe")
axes[0].legend()
axes[0].set_ylim(0, 1.05)
axes[0].grid(True, axis="y", alpha=0.3)

cm_tl = confusion_matrix(y_test_classes, y_pred_tl)
sns.heatmap(cm_tl, annot=True, fmt="d", cmap="Greens", ax=axes[1],
            xticklabels=CLASSES, yticklabels=CLASSES, linewidths=0.4)
axes[1].set_title(f"Confusion Matrix — MobileNetV2  (Acc={acc_tl*100:.2f}%)")
axes[1].set_xlabel("Predição")
axes[1].set_ylabel("Real")
plt.setp(axes[1].get_xticklabels(), rotation=35, ha="right")
plt.tight_layout()
plt.savefig("cnn_comparacao.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_comparacao.png")

# Curvas do Transfer Learning (fases concatenadas)
hist_tl_combinado = {
    k: hist_f1.history.get(k, []) + hist_f2.history.get(k, [])
    for k in ["loss", "val_loss", "accuracy", "val_accuracy"]
}
plot_historico(hist_tl_combinado,
               "MobileNetV2 — Curvas (Fase 1 + Fase 2)",
               "cnn_tl_curvas.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 9 — SERIALIZAÇÃO (.keras + .pkl) E INFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[9/10] Salvando modelos e realizando inferência...")

modelo_baseline.save(MODEL_BASELINE_PATH)
modelo_tl.save(MODEL_TL_PATH)

joblib.dump({
    "baseline": hist_baseline.history,
    "tl_f1":    hist_f1.history,
    "tl_f2":    hist_f2.history,
    "acc_base": float(acc_base),
    "acc_tl":   float(acc_tl),
    "classes":  CLASSES,
}, HISTORICO_PATH)

print(f"  Baseline salvo:        {MODEL_BASELINE_PATH}")
print(f"  Transfer L. salvo:     {MODEL_TL_PATH}")
print(f"  Histórico pkl salvo:   {HISTORICO_PATH}")

# Carregar do disco e inferir
modelo_carregado = keras.models.load_model(MODEL_TL_PATH)
print(f"\n  Modelo carregado do disco com sucesso.")

# 12 imagens de teste (2 por classe, 6 primeiras classes)
idx_inf = []
for cls in range(6):
    idx_inf.extend(np.where(y_test_classes == cls)[0][:2].tolist())

X_inf = X_test[idx_inf]
y_inf = y_test_classes[idx_inf]
probs = modelo_carregado.predict(X_inf, verbose=0)
preds = np.argmax(probs, axis=1)
confs = probs.max(axis=1)

print(f"\n  {'#':>4}  {'Real':12s}  {'Predição':12s}  {'Conf':>7}  {'OK'}")
print(f"  {'─'*50}")
for i in range(len(X_inf)):
    ok = "✓" if y_inf[i] == preds[i] else "✗"
    print(f"  {i+1:>4}  {CLASSES[y_inf[i]]:12s}  {CLASSES[preds[i]]:12s}  "
          f"{confs[i]*100:6.1f}%  {ok}")

fig, axes = plt.subplots(2, 6, figsize=(14, 5))
fig.suptitle("Inferência — MobileNetV2 Transfer Learning",
             fontsize=13, fontweight="bold")
for i, ax in enumerate(axes.flat):
    ax.imshow(X_inf[i])
    cor = "green" if y_inf[i] == preds[i] else "red"
    ax.set_title(f"Pred: {CLASSES[preds[i]]}\n{confs[i]*100:.1f}%",
                 fontsize=8, color=cor, fontweight="bold")
    ax.set_xlabel(f"Real: {CLASSES[y_inf[i]]}", fontsize=7)
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig("cnn_inferencia.png", dpi=110, bbox_inches="tight")
plt.close()
print("  Salvo: cnn_inferencia.png")

# ─────────────────────────────────────────────────────────────────────────────
# ETAPA 10 — GRAD-CAM
# ─────────────────────────────────────────────────────────────────────────────
print("\n[10/10] Grad-CAM — Explicabilidade Visual...")

# Localizar backbone MobileNetV2 dentro do modelo carregado
backbone_loaded = None
for layer in modelo_carregado.layers:
    if "mobilenetv2" in layer.name.lower():
        backbone_loaded = layer
        break

if backbone_loaded is not None:
    # Última camada Conv2D do backbone
    ultima_conv = next(
        (l.name for l in reversed(backbone_loaded.layers)
         if isinstance(l, layers.Conv2D)), None
    )

    if ultima_conv:
        # Modelo auxiliar: backbone_input → (última conv, backbone_output)
        grad_model = Model(
            inputs=backbone_loaded.input,
            outputs=[
                backbone_loaded.get_layer(ultima_conv).output,
                backbone_loaded.output,
            ]
        )

        # Selecionar 1 imagem por classe (10 imagens)
        imgs_gc, labels_gc = [], []
        for cls in range(NUM_CLASSES):
            idx = np.where(y_test_classes == cls)[0][0]
            imgs_gc.append(X_test[idx])
            labels_gc.append(cls)

        fig, axes = plt.subplots(3, NUM_CLASSES, figsize=(20, 7))
        fig.suptitle("Grad-CAM — Regiões de Ativação por Classe",
                     fontsize=14, fontweight="bold")

        for i, (img, lbl) in enumerate(zip(imgs_gc, labels_gc)):
            # Preparar input para o backbone (upscale + preprocess)
            img_up = tf.image.resize(img[np.newaxis], [96, 96]).numpy()
            img_up_p = tf.keras.applications.mobilenet_v2.preprocess_input(
                img_up * 255.0
            )

            # Calcular gradientes
            with tf.GradientTape() as tape:
                img_t = tf.cast(img_up_p, tf.float32)
                conv_out, bb_out = grad_model(img_t)
                pred_idx = tf.argmax(bb_out[0])
                class_score = bb_out[:, pred_idx]

            grads = tape.gradient(class_score, conv_out)
            pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
            heatmap = (conv_out[0] @ pooled[..., tf.newaxis]).numpy().squeeze()
            heatmap = np.maximum(heatmap, 0)
            heatmap /= (heatmap.max() + 1e-8)

            # Redimensionar heatmap para 32×32
            hm32 = tf.image.resize(
                heatmap[..., np.newaxis], [32, 32]
            ).numpy().squeeze()
            hm32 /= (hm32.max() + 1e-8)

            # Sobreposição colorida
            jet = plt.cm.jet(np.arange(256))[:, :3]
            hm_c = jet[np.uint8(255 * hm32)]
            over = (hm_c * 0.45 + img * 0.55).clip(0, 1)

            # Predição global
            pred_global = modelo_carregado.predict(img[np.newaxis], verbose=0)
            pred_cls = int(np.argmax(pred_global))
            conf_g = float(pred_global.max()) * 100
            cor_t = "green" if pred_cls == lbl else "red"

            axes[0, i].imshow(img)
            axes[0, i].set_title(
                f"{CLASSES[lbl]}", fontsize=7, fontweight="bold")
            axes[0, i].axis("off")

            axes[1, i].imshow(hm32, cmap="jet")
            axes[1, i].set_title("heatmap", fontsize=7)
            axes[1, i].axis("off")

            axes[2, i].imshow(over)
            axes[2, i].set_title(f"{CLASSES[pred_cls]}\n{conf_g:.0f}%",
                                 fontsize=7, color=cor_t, fontweight="bold")
            axes[2, i].axis("off")

        for row, lbl_row in enumerate(["Original", "Grad-CAM", "Sobreposição"]):
            axes[row, 0].set_ylabel(lbl_row, fontsize=9, fontweight="bold",
                                    rotation=90, labelpad=40, va="center")

        plt.tight_layout()
        plt.savefig("cnn_gradcam.png", dpi=110, bbox_inches="tight")
        plt.close()
        print("  Salvo: cnn_gradcam.png")
    else:
        print("  [Grad-CAM] Camada Conv2D não localizada no backbone.")
else:
    print("  [Grad-CAM] Backbone MobileNetV2 não encontrado no modelo carregado.")

# ─────────────────────────────────────────────────────────────────────────────
# RESUMO FINAL
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  RESUMO FINAL")
print("=" * 70)
print(
    f"  Dataset          : CIFAR-10  ({X_train_.shape[0]} treino / {X_test.shape[0]} teste)")
print(
    f"  CNN Baseline     : {acc_base*100:.2f}% accuracy  |  {modelo_baseline.count_params():,} parâmetros")
print(
    f"  MobileNetV2 (TL) : {acc_tl*100:.2f}% accuracy  |  fine-tuning 2 fases")
print(f"  Ganho TL         : +{(acc_tl-acc_base)*100:.2f} pp")
print(f"\n  Arquivos gerados:")
arquivos = [
    MODEL_BASELINE_PATH, MODEL_TL_PATH, HISTORICO_PATH,
    "cnn_eda_amostras.png", "cnn_eda_distribuicao.png",
    "cnn_augmentation.png", "cnn_baseline_curvas.png",
    "cnn_baseline_confusion.png", "cnn_tl_curvas.png",
    "cnn_comparacao.png", "cnn_inferencia.png", "cnn_gradcam.png",
    "cnn_baseline_log.csv", "cnn_tl_log.csv",
]
for f in arquivos:
    print(f"    {f}")
print("\n" + "=" * 70)
print("  CNN — DEEP LEARNING CONCLUÍDO COM SUCESSO")
print("=" * 70)
