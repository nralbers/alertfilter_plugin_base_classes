import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    METRICS_START_PORT=(int, 5001),
    GUNICORN_WORKERS=(int, 5),
)
environ.Env.read_env(env_file=str(BASE_DIR / ".env"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_KEY", default="-!n@hv_xvh$&&=su9x9c2_m6o_z+xr91i4$bgp)f!=6jd_b1x)"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.base_classes",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

ROOT_URLCONF = "django_app.urls"

WSGI_APPLICATION = "django_app.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django_app.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django_app.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django_app.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django_app.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env(
            "DB_ENGINE", default="django.db.backends.sqlite3"
        ),  # 'django.db.backends.mysql'
        "NAME": env("DB_NAME", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env("DB_USER", default=None),
        "PASSWORD": env("DB_PASSWORD", default=None),
        "HOST": env(
            "DB_HOST", default=None
        ),  # Or an IP Address that your DB is hosted on
        "PORT": env("DB_PORT", default=None),  # '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#
# # Test Runner
# TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application name in snake_case for Prometheus metric prefix
APPLICATION_NAME = "alert_filter"
