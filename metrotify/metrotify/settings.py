"""
Django settings for metrotify project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import pymongo
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^#5$&uw7+%fl&^=!pj^xsiuum++$nkv045-6tc_4l=u273#uv#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS = (
     'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'aplicacion.usuario', 
    'aplicacion.musical', 
    'aplicacion.indicadores', 
    'aplicacion.interaciones', 
)

THIRD_PARTY_APPS = (
    'rest_framework',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'metrotify.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'metrotify.wsgi.application'


URI="mongodb://metrotifydb:fw4MRwLQ4hoXONg5@ac-znymkzd-shard-00-00.ysigne7.mongodb.net:27017,ac-znymkzd-shard-00-01.ysigne7.mongodb.net:27017,ac-znymkzd-shard-00-02.ysigne7.mongodb.net:27017/?ssl=true&replicaSet=atlas-14cc8j-shard-0&authSource=admin&retryWrites=true&w=majority&appName=metrotify"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'metrotify',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host':URI,
        }
    }
}
# Connect to a MongoDB Atlas cluster (replace with your credentials)
#client = pymongo.MongoClient("URI")

# # Access a specific database
# database = client["metrotify02"]

#PQG2hJntTJ56LBNn
#PQG2hJntTJ56LBNn
#WzCeZc6KOmmrQvEa
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

#metrotifydb
#fw4MRwLQ4hoXONg5
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-VE'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'usuario.User'
#AUTH_USER_MODEL = 'auth.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for mixin loginrequiredmixin in view home, LoginView, LogoutView
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

