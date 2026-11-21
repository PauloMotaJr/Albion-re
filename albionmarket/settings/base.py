"""
Configuração base Django carregada via variáveis de ambiente.
Usa valores padrão do .env quando não definidos explicitamente.
"""

import os
from pathlib import Path

# Build path absoluto para templates estáticos e arquivos de mídia
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configuração do Django
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Application list
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]

# Middleware padrão do Django
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuração de URLs do Django
ROOT_URLCONF = "albionmarket.urls"

WSGI_APPLICATION = "albionmarket.wsgi.application"

# Dados do Banco de Dados PostgreSQL - usa 'db' como host (nome do container)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "albion_market"),
        "USER": os.environ.get("DB_USER", "albin_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),  # Deverá ser definido no .env
        "HOST": "db",  # Nome do container PostgreSQL
        "PORT": "5432",
    }
}

# Configuração de templates base
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(BASE_DIR) / "templates"],  # Templates em pasta raiz do projeto
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Configuração de Internationalização (desativada por padrão)
USE_I18N = False
USE_L10N = False
USE_TZ = True
TIME_ZONE = "UTC"

# Logging básico
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{}"},},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": LOG_LEVEL,
        },
    },
    "loggers": {
        "albionmarket": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}

# Static Files - pasta de templates em raiz do projeto
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media Files (uploads - vazio inicialmente)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Variáveis de ambiente para Django
if DEBUG:
    SECURE_SSL_REDIRECT = False
else:
    SECURE_SSL_REDIRECT = True
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True