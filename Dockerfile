FROM ghcr.io/astral-sh/uv AS uv

FROM python:3.10-slim
ARG TARGETARCH
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar pacotes necessários
RUN apt-get update && apt-get install curl streamlink chromium -y

# Copiar o pyproject.toml
COPY pyproject.toml .

# Gerar requirements.txt com pip-compile
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

ENTRYPOINT [ "python", "manage.py" ]
