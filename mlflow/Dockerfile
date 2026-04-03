FROM python:3.12-slim

# Evita a geração de arquivos .pyc e força o log a aparecer no terminal sem atrasos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cria um usuário não-root para maior segurança
RUN adduser --disabled-password --gecos "" mlflow_user

WORKDIR /mlflow/

# Instala as dependências
RUN pip install --no-cache-dir mlflow boto3 pymysql psycopg2-binary

# Cria as pastas para os artefatos e banco de dados, e ajusta permissões
RUN mkdir -p /mlflow/mlruns /mlflow/data && \
    chown -R mlflow_user:mlflow_user /mlflow

# Muda para o usuário seguro
USER mlflow_user

EXPOSE 5000

# Healthcheck usando o próprio Python para garantir que o serviço está respondendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || exit 1

# O CMD agora pega os valores que serão passados pelo .env via Docker Compose
CMD mlflow server \
    --backend-store-uri ${BACKEND_URI} \
    --default-artifact-root ${ARTIFACT_ROOT} \
    --host 0.0.0.0 \
    --port 5000