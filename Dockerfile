FROM ghcr.io/astral-sh/uv AS uv

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instalar pacotes necessários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar o pyproject.toml
COPY pyproject.toml .

# Gerar requirements.txt com pip-compile
RUN pip install pip-tools
RUN pip-compile --output-file=requirements.txt pyproject.toml

# Instalar dependências usando uv
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    apt-get -y install gcc musl-dev && \
    uv pip install --system -r requirements.txt && \
    apt-get -y autoremove gcc musl-dev && apt-get clean

# Copiar o código da aplicação
COPY . .

# Instalar o código da aplicação no ambiente
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    uv pip install --system -e .

# Configurar Gunicorn como servidor WSGI para produção
RUN pip install gunicorn

# Comando de inicialização para o ambiente de produção com Gunicorn
CMD ["gunicorn", "garopabus.wsgi:application", "--bind", "0.0.0.0:8022", "--workers", "4", "--threads", "2"]
