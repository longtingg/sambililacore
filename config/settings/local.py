from .base import *
from .base import env


DEBUG = True
SSL_ISSANDBOX = env('SSL_ISSANDBOX', default=True)
STORE_ID = env('STORE_ID', default='')
STORE_PASS = env('STORE_PASS', default='')

THIRD_PARTY_APPS += [
    'debug_toolbar',
]
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1', '::1'])

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}
