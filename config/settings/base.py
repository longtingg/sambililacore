import os
from pathlib import Path
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.core.exceptions import ImproperlyConfigured
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
ALLOWED_HOSTS = ['*']  # Required for Replit
CSRF_TRUSTED_ORIGINS = ['https://*.replit.dev', 'https://*.repl.co']

# Application Definition
INSTALLED_APPS = [
    'django_school_management.accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
] + [
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
] + [
    'rest_framework', 'corsheaders', 'crispy_forms', 'crispy_bootstrap4',
    'rolepermissions', 'taggit', 'django_extensions', 'django_filters',
    'allauth', 'allauth.account', 'allauth.socialaccount', 'ckeditor',
    'ckeditor_uploader', 'mptt', 'widget_tweaks', 'django_social_share',
    'django_countries', 'import_export', 'django_tables2', 'bootstrap4',
    'django_file_form', 'tinymce', 'drf_yasg', 'django_rest_passwordreset',
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essential for Replit static
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

# Database - Flexible for Replit/Production
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}

# Static/Media for Replit
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
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Email/Redirects
LOGIN_REDIRECT_URL = AccountURLConstants.profile_complete
LOGIN_URL = AccountURLConstants.profile_complete

# Final check
if env('USE_SENTRY', default=False):
    sentry_sdk.init(dsn=env('SENTRY_DSN'), integrations=[DjangoIntegration()])
