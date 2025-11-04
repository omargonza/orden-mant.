from pathlib import Path
import os
from dotenv import load_dotenv

# 🔹 Carga variables del archivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Configuración básica
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "orden-mant.onrender.com,localhost,127.0.0.1").split(",")

# 🔸 Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "orders",
]

# 🔸 Middlewares (⚠️ sin duplicar corsheaders)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # ya insertado en la posición correcta
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 🔸 CORS y CSRF
CORS_ALLOWED_ORIGINS = [
    "https://orden-mant-frontend.onrender.com",
]
CSRF_TRUSTED_ORIGINS = [
    "https://orden-mant.onrender.com",
    "https://orden-mant-frontend.onrender.com",
]

# ⚠️ No uses CORS_ALLOW_ALL_ORIGINS=True en prod, lo mantenemos solo si DEBUG=True
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# 🔸 URL principal
ROOT_URLCONF = "core.urls"

# 🔸 Templates
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

# 🔸 WSGI
WSGI_APPLICATION = "core.wsgi.application"

# 🔸 Base de datos
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
    }
}

# 🔸 Internacionalización
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# 🔸 Archivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# 🔸 WhiteNoise para servir estáticos en Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🔸 Archivos subidos (si usás media)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 🔸 Campo por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ✅ Puerto para Render (no es necesario si usás gunicorn)
PORT = int(os.environ.get("PORT", 10000))
