"""
Django settings for VentaEntradas project.
Generado por 'django-admin startproject' usando Django 3.2.24.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR apunta a /src
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde el archivo .env.db ubicado en la raíz del proyecto
env_path = BASE_DIR.parent / ".env.db"
load_dotenv(dotenv_path=env_path)

# Clave secreta de Django
SECRET_KEY = "django-insecure-@ed-zzj52v1tp0eetl+r_)utc8t+2zyw2(jkb#94pg_sd!(#6%"

# Modo de depuración
DEBUG = True

# Hosts permitidos
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "VentaEntradas",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuración de URLs y WSGI
ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

# Configuración de templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Configuración de bases de datos
DATABASES = {
    # MongoDB (djongo)
    "default": {
        "ENGINE": "djongo",
        "NAME": "mongo",
        "CLIENT": {
            "host": "mongo",
            "port": 27017,
            "username": "mongo",
            "password": "mongo",
            "authSource": "admin",
        },
    },
    # PostgreSQL (origen de datos relacional)
    "old_db": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "VentaEntrada",           # ← Cambiado para apuntar a la base real
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "db",                 # nombre del servicio en docker-compose
        "PORT": "5432",
    },
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configuración regional
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "/static/"

# Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
