from os import getenv
from pathlib import Path
from random import choices
from string import ascii_letters

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DOMAIN = getenv("DOMAIN", "127.0.0.1:8000")
EMAIL_API_KEY = getenv("EMAIL_API_KEY")
DEFAULT_EMAIL_SENDER = getenv("DEFAULT_EMAIL_SENDER")

RANDOM_KEY = "".join(choices(ascii_letters, k=128))
DJANGO_SECRET = getenv("DJANGO_SECRET")
SECRET_KEY = DJANGO_SECRET or RANDOM_KEY

if DJANGO_SECRET:
    DEBUG = False
    FORCE_SCRIPT_NAME = "/moonseacodex/"
    ADMIN_URL = "/moonseacodex/admin"
else:
    DEBUG = True

SERVER = getenv("SERVER")
ALLOWED_HOSTS = ["127.0.0.1"] if SERVER else []
CSRF_TRUSTED_ORIGINS = [f"https://{SERVER}"] if SERVER else []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "codex",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "core.wsgi.application"

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": getenv("DB_USER"),
            "PASSWORD": getenv("DB_PASS"),
            "HOST": getenv("DB_HOST"),
            "PORT": "5432",
        }
    }

AUTH_USER_MODEL = "codex.CodexUser"
AUTHENTICATION_BACKENDS = ["codex.utils.backends.CustomUserModelBackend"]

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "codex.utils.security.SessionCSRFExemptAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
APPEND_SLASH = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "admin_static/"
STATIC_ROOT = BASE_DIR / "admin_static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = "smtp.sendgrid.net"
DEFAULT_FROM_EMAIL = DEFAULT_EMAIL_SENDER
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = EMAIL_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
