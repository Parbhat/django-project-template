from .base import *


ENVIRONMENT = 'development'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = not DEBUG

ALLOWED_HOSTS = ['*',]

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = globals().get('INSTALLED_APPS', [])
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = globals().get('MIDDLEWARE_CLASSES', [])
MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ project_name }}',
        'USER': '{{ project_name }}',
        'PASSWORD': env_setting('{{ project_name|upper }}_DB_PASSWORD'),
        'HOST': env_setting('{{ project_name|upper }}_DB_SERVER'),
        'PORT': '3306',
    }
}

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    'LOCATION': local_join('..', '_tmp', 'django_cache'),
}

LOGGING['handlers']['console']['formatter'] = 'simple'
LOGGING['handlers']['console']['level'] = 'DEBUG'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
