import dj_database_url
import environ
import os

env = environ.Env()
environ.Env.read_env()

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
ADMIN_EMAIL = env("ADMIN_EMAIL")
EMAIL_USE_TLS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "birthday.apps.BirthdayConfig",
    "staffapp.apps.StaffappConfig",
    "django.contrib.postgres",
    "phonenumber_field",
    "django_browser_reload",
    "widget_tweaks",
    "debug_toolbar",
    "django_htmx",
    "mathfilters",
    "active_link",
    "tailwind",
    "theme",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "mitcbdayapp.middleware.BrowserReloadMiddleware",
    # "livesync.core.middleware.DjangoLiveSyncMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# SESSION_EXPIRE_SECONDS = 20  # seconds
# SESSION_TIMEOUT_REDIRECT = "index"
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = "mitcbdayapp.urls"
TAILWIND_APP_NAME = "theme"
TAILWIND_CSS_PATH = "css/dist/styles.css"
INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = r"C:/Program Files/nodejs/npm.cmd"

# Template Directories
ROOT = os.path.join(BASE_DIR, "templates")
BIRTHDAY = os.path.join(BASE_DIR, "birthday/templates/")
STAFFAPP = os.path.join(BASE_DIR, "staffapp/templates/")
THEME = os.path.join(BASE_DIR, "theme/templates/")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ROOT, BIRTHDAY, STAFFAPP, THEME],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.media",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images etc)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Location of static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Location of media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

BIRTHDAY_STATIC = os.path.join(BASE_DIR, "birthday/templates/static/")
STAFFAPP_STATIC = os.path.join(BASE_DIR, "staffapp/static/staffapp")
THEME_STATIC = os.path.join(BASE_DIR, "theme/static/theme")
STATICFILES_DIRS = [
    MEDIA_ROOT,
    BIRTHDAY_STATIC,
    STAFFAPP_STATIC,
    THEME_STATIC
]

WSGI_APPLICATION = "mitcbdayapp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL"), conn_max_age=600, conn_health_checks=True
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Phone Number
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_REGION = "NG"
PHONENUMBER_DEFAULT_FORMAT = "E164"
