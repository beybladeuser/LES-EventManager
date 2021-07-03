"""
Django settings for EventManager project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from django.conf import settings
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ro$#oej!7^k1-*1^oe=k#g3o@!y#=d+rkw^op@f!^4gtrx#wnk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'Models.apps.ModelsConfig',
    'FormManagement.apps.FormmanagementConfig',
    'AssetManagement.apps.AssetmanagementConfig',
    'EventManagement.apps.EventmanagementConfig',
    'PreEventManagement.apps.PreeventmanagementConfig',
    'Schedules.apps.SchedulesConfig',
    # 'Sessions.apps.SessionsConfig',
    'utilizadores.apps.UtilizadoresConfig',
    'Index.apps.IndexConfig',
    'crispy_forms',
    'django_tables2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notificacoes',
    'notifications',
    'clear_cache',
]

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}

NOTIFICATIONS_NOTIFICATION_MODEL = 'notificacoes.Notificacao'
CONFIG_DEFAULTS = {
    'PAGINATE_BY': 20,
    'USE_JSONFIELD': False,
    'SOFT_DELETE': False,
    'NUM_TO_FETCH': 10,
}


def get_config():
    user_config = getattr(settings, 'DJANGO_NOTIFICATIONS_CONFIG', {})

    config = CONFIG_DEFAULTS.copy()
    config.update(user_config)

    return config

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EventManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EventManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eventmanager',
        'USER' : 'root',
        'PASSWORD' : '',
        'HOST' : '127.0.0.1',
        'PORT' : '3307',
        'OPTIONS' : {
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS is for development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


CRISPY_TEMPLATE_PACK="bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

USE_L10N = False
DATETIME_FORMAT = 'd/m/Y H:i:s'