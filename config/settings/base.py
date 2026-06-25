import os
from pathlib import Path
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.contrib.messages import constants as messages
from django_school_management.accounts.constants import AccountURLConstants

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Env Setup
env = environ.Env(
    DEBUG=(bool, False),
    USE_PAYMENT_OPTIONS=(bool, False),
    USE_SENTRY=(bool, False),
)
env.read_env(str(BASE_DIR / "envs/.env"))

# Core Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.replit.dev', 'https://*.repl.co']

# Application Definition - split into groups for local/production overrides
DEFAULT_APPS = [
    'django_school_management.accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'django_school_management.students.apps.StudentsConfig',
    'django_school_management.teachers.apps.TeachersConfig',
    'django_school_management.result.apps.ResultConfig',
    'django_school_management.academics.apps.AcademicsConfig',
    'django_school_management.pages.apps.PagesConfig',
    'django_school_management.articles.apps.ArticlesConfig',
    'django_school_management.institute.apps.InstituteConfig',
    'django_school_management.curriculum.apps.CurriculumConfig',
    'django_school_management.payments.apps.PaymentsConfig',
    'django_school_management.notices.apps.NoticesConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework', 'corsheaders', 'crispy_forms', 'crispy_bootstrap4',
    'rolepermissions', 'taggit', 'django_extensions', 'django_filters',
    'allauth', 'allauth.account', 'allauth.socialaccount', 'ckeditor',
    'ckeditor_uploader', 'mptt', 'widget_tweaks', 'django_social_share',
    'django_countries', 'import_export', 'django_tables2', 'bootstrap4',
    'django_file_form', 'tinymce', 'drf_yasg', 'django_rest_passwordreset',
    'django_prometheus',
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static/Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Replit Proxy Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Standard Auth/Site Config
SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django_school_management.accounts.backends.MultiIdentifierBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_FORMS = {
    'login': 'django_school_management.accounts.forms.SCESLoginForm',
}

# Email/Redirects
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Django Admin URL
DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin')

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor
CKEDITOR_UPLOAD_PATH = 'uploads/'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Message tags
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

if env('USE_SENTRY', default=False):
    sentry_sdk.init(dsn=env('SENTRY_DSN', default=''), integrations=[DjangoIntegration()])
