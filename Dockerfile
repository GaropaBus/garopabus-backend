FROM ghcr.io/astral-sh/uv AS uv

FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependências do sistema necessárias para o Django
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas os arquivos necessários para instalação de dependências
COPY pyproject.toml .

# Instalar dependências usando UV
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    uv pip install --system -r pyproject.toml && \
    apt-get purge -y gcc && apt-get autoremove -y && apt-get clean

# Copiar o resto do projeto
COPY . .

# Instalar o projeto em modo editável
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    uv pip install --system -e .

# Coletar arquivos estáticos
COPY .env .env
RUN python manage.py collectstatic --noinput
RUN rm -f .env

# Expor a porta que o Gunicorn vai rodar
EXPOSE 8022

# Comando para rodar com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8022", "garopabus.wsgi:application"]