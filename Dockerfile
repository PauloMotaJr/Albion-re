FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Instalação de dependências system (antes de criar usuário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configuração de usuário NÃO-ROOT
RUN groupadd --gid 1000 albion && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home albion

WORKDIR /app

# Instalação de dependências Python (como root ainda)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configuração do ambiente Django
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=albionmarket.settings.base

# Switch para usuário não-root + copia do código
USER albion
COPY --chown=albion:albion . .

# Comandos de execução (como usuário albion)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "albionmarket.wsgi:application"]