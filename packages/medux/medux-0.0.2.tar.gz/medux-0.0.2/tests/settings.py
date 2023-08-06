"""
Django test ettings for medux project.
"""

import environ
from pathlib import Path
from gdaps.pluginmanager import PluginManager


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = "medux"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "test-secret-value"

DEBUG = False

ALLOWED_HOSTS = ["localhost"]

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "menu",
    "graphene_django",
    # "channels",
    # "gdaps.graphene",
    "gdaps",
    "rest_framework",
    "django_filters",
    "django_unicorn",
]

# Note: Plugins that are included per default within this repository
# should be added to the [options.entry_points] section in MdeUX' setup.cfg
INSTALLED_APPS += PluginManager.find_plugins("medux.plugins")

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "core.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "medux.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "medux" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            # "builtins": ["django_component.templatetags"],
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS = ["django.core.context_processors.request"]
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-FORM_RENDERER
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "medux.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "de-AT"

TIME_ZONE = "Europe/Vienna"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = BASE_DIR / "media"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "gdaps": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        # "django.template": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": True,
        # },
        "unicorn": {"handlers": ["console"], "level": "INFO"},
        "medux": {"handlers": ["console"], "level": "DEBUG"},
    },
}


# GDAPS configuration
GDAPS = {}

# not needed ATM
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#         # "BACKEND": "channels_redis.core.RedisChannelLayer",
#         # "CONFIG": {
#         #     "hosts": [("127.0.0.1", 6379)],
#         # },
#     },
# }

ASGI_APPLICATION = "medux.asgi.application"

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#       "rest_framework.permissions.DjangoModelPermissions"
#     ]
# }
