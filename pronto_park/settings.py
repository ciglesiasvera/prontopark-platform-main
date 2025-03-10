from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#ALLOWED_HOSTS = os.getenv('prontopark-platform-main.onrender.com','DJANGO_ALLOWED_HOSTS', '').split(',')
#ALLOWED_HOSTS = ['prontopark-platform-main.onrender.com','127.0.0.1']

# Asegúrate de que DEBUG esté desactivado en producción:
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Configura ALLOWED_HOSTS correctamente:
ALLOWED_HOSTS = ["prontopark-platform-main.onrender.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "parkings",
    "residences",
    "reservations",
    "home",
    "alerts",
    "reports",
    "dashboards",
    #'django_cron',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pronto_park.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pronto_park.context_processors.global_context",
            ],
        },
    },
]


WSGI_APPLICATION = "pronto_park.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import dj_database_url

# Reemplaza tu configuración actual de DATABASES con esto:
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

""" DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
} """

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static/",
]

# Media files (User-uploaded content)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CRON_CLASSES = [
#    "reservations.cron.MyCronJob",
# ]

# Configuración del modelo de usuario personalizado
AUTH_USER_MODEL = "users.User"

# Configuración del backend de autenticación
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
