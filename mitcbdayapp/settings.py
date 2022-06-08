"""
Django settings for mitcbdayapp project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import environ, os
from pathlib import Path


env = environ.Env()
environ.Env.read_env()


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
ADMIN_EMAIL = env('ADMIN_EMAIL')
EMAIL_USE_TLS = True


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=it7f$tmb#vy=11%1$-%&91*6s_^!5mu5mtgo2rir1int%y0lt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sendmail.apps.SendmailConfig',
    'phonenumber_field',
    'tailwind',
    'theme',
    'django_browser_reload',
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'mitcbdayapp.urls'
TAILWIND_APP_NAME = 'theme'
TAILWIND_CSS_PATH = 'css/dist/styles.css'
INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = r"C:/Program Files/nodejs/npm.cmd"


# Template Directories
ROOT = os.path.join(BASE_DIR, 'templates')
SENDMAIL = os.path.join(BASE_DIR, 'sendmail/templates/')
THEME = os.path.join(BASE_DIR, 'theme/templates/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT, SENDMAIL, THEME],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]



# Static files (CSS, JavaScript, Images etc)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Location of static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
SENDMAIL_STATIC = os.path.join(BASE_DIR, "sendmail/templates/static/")
THEME_STATIC = os.path.join(BASE_DIR, "theme/static/")
STATICFILES_DIRS = [SENDMAIL_STATIC, THEME_STATIC]


# Location of media files

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = [ MEDIA_ROOT ]


WSGI_APPLICATION = 'mitcbdayapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,  'db.sqlite3'),
    
    'OPTIONS': {'timeout': 20}    
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English')
]
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Phone Number 
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'NG'
PHONENUMBER_DEFAULT_FORMAT = 'E164'
