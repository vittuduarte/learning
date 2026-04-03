# %%
#!pip install -r requirements.txt
# %%
import matplotlib.pyplot as plt
from feature_engine import discretisation, encoding
import mlflow
from sklearn import metrics
from sklearn import pipeline
from sklearn import ensemble
from sklearn import model_selection
from sklearn import tree
import pandas as pd

# %%


mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment(experiment_id='1')
mlflow.set_experiment(experiment_name='Biofogo-teste-random-forest')

pd.options.display.max_columns = 500
pd.options.display.max_rows = 500
# %%
df = pd.read_csv("../data/abt_churn.csv")
df.head()

# %%
oot = df[df["dtRef"] == df['dtRef'].max()].copy()
df_train = df[df["dtRef"] < df['dtRef'].max()].copy()

# %%

# Essas são as variáveis
features = df_train.columns[2:-1]

# Essa é a nossa target
target = 'flagChurn'

X, y = df_train[features], df_train[target]


# %%
# SAMPLE

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y,
                                                                    random_state=42,
                                                                    test_size=0.2,
                                                                    stratify=y,
                                                                    )

print("Taxa variável resposta geral:", y.mean())
print("Taxa variável resposta Treino:", y_train.mean())
print("Taxa variável resposta Test:", y_test.mean())

# %%

# EXPLORE (MISSINGS)

X_train.isna().sum().sort_values(ascending=False)

# %%

# EDA dos dados numéricos para entender a relação com a variável resposta

df_analise = X_train.copy()
df_analise[target] = y_train
summario = df_analise.groupby(by=target).agg(["mean", "median"]).T
summario['diff_abs'] = summario[0] - summario[1]
summario['diff_rel'] = summario[0] / summario[1]
summario.sort_values(by=['diff_rel'], ascending=False)

# %%

# Utilizamos uma árvore de decisão para entender a importância das variáveis e selecionar as mais relevantes para o modelo

arvore = tree.DecisionTreeClassifier(random_state=42)
arvore.fit(X_train, y_train)

feature_importances = (pd.Series(arvore.feature_importances_,
                                 index=X_train.columns)
                       .sort_values(ascending=False)
                       .reset_index()
                       )

feature_importances['acum.'] = feature_importances[0].cumsum()
feature_importances[feature_importances['acum.'] < 0.96]

# %%

# Selecionamos as variáveis que, juntas, explicam 96% da importância total

best_features = (feature_importances[feature_importances['acum.'] < 0.96]['index']
                 .tolist())

best_features

# %%
# MODIFY

# Discretizar as variáveis numéricas utilizando uma árvore de decisão para encontrar os melhores pontos de corte, considerando a relação com a variável resposta
tree_discretization = discretisation.DecisionTreeDiscretiser(
    variables=best_features,
    regression=False,
    bin_output='bin_number',
    cv=3,
)

# Onehot
onehot = encoding.OneHotEncoder(variables=best_features, ignore_format=True)

# %%
# MODEL

with mlflow.start_run():

    mlflow.sklearn.autolog()

    model = ensemble.RandomForestClassifier(
        random_state=42,
        n_jobs=2,
    )

    params = {
        "min_samples_leaf": [15, 20, 25, 30, 50],
        "n_estimators": [100, 200, 500, 1000],
        "criterion": ['gini', 'entropy', 'log_loss'],
    }

    grid = model_selection.GridSearchCV(model,
                                        params,
                                        cv=3,
                                        scoring='roc_auc',
                                        verbose=4,
                                        )

    model_pipeline = pipeline.Pipeline(
        steps=[
            ('Discretizar', tree_discretization),
            ('Onehot', onehot),
            ('Grid', grid),
        ]
    )

    model_pipeline.fit(X_train[best_features], y_train)

    # ASSESS
    y_train_predict = model_pipeline.predict(X_train[best_features])
    y_train_proba = model_pipeline.predict_proba(X_train[best_features])[:, 1]

    acc_train = metrics.accuracy_score(y_train, y_train_predict)
    auc_train = metrics.roc_auc_score(y_train, y_train_proba)
    roc_train = metrics.roc_curve(y_train, y_train_proba)
    print("Acurácia Treino:", acc_train)
    print("AUC Treino:", auc_train)

    y_test_predict = model_pipeline.predict(X_test[best_features])
    y_test_proba = model_pipeline.predict_proba(X_test[best_features])[:, 1]

    acc_test = metrics.accuracy_score(y_test, y_test_predict)
    auc_test = metrics.roc_auc_score(y_test, y_test_proba)
    roc_test = metrics.roc_curve(y_test, y_test_proba)
    print("Acurácia Test:", acc_test)
    print("AUC Test:", auc_test)

    y_oot_predict = model_pipeline.predict(oot[best_features])
    y_oot_proba = model_pipeline.predict_proba(oot[best_features])[:, 1]

    acc_oot = metrics.accuracy_score(oot[target], y_oot_predict)
    auc_oot = metrics.roc_auc_score(oot[target], y_oot_proba)
    roc_oot = metrics.roc_curve(oot[target], y_oot_proba)
    print("Acurácia oot:", acc_oot)
    print("AUC oot:", auc_oot)

    mlflow.log_metrics({
        "acc_train": acc_train,
        "auc_train": auc_train,
        "acc_test": acc_test,
        "auc_test": auc_test,
        "acc_oot": acc_oot,
        "auc_oot": auc_oot,
    })

# %%

plt.figure(dpi=400)
plt.plot(roc_train[0], roc_train[1])
plt.plot(roc_test[0], roc_test[1])
plt.plot(roc_oot[0], roc_oot[1])
plt.plot([0, 1], [0, 1], '--', color='black')
plt.grid(True)
plt.ylabel("Sensibilidade")
plt.xlabel("1 - Especificidade")
plt.title("Curva ROC")
plt.legend([
    f"Treino: {100*auc_train:.2f}",
    f"Teste: {100*auc_test:.2f}",
    f"Out-of-Time: {100*auc_oot:.2f}",
])

plt.show()
