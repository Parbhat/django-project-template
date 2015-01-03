from .base import *

ENVIRONMENT = 'production'
ALLOWED_HOSTS = ['.{{ project_name }}',]

DEBUG = False
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_JS_FILTERS = []

USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True

INSTALLED_APPS = globals().get('INSTALLED_APPS', [])
INSTALLED_APPS += [
    'gunicorn',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ project_name }}',
        'USER': 'root',
        'PASSWORD': env_setting('{{ project_name|upper }}_DB_PASSWORD'),
        'HOST': env_setting('{{ project_name|upper }}_DB_SERVER'),
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '%s:0' % env_setting('{{ project_name|upper }}_REDIS_SERVER'),
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        },
    },
}

# Logging settings
LOGGING['handlers']['syslog'] = {
    'class': 'logging.handlers.SysLogHandler',
    'formatter': 'verbose',
    'level': 'INFO',
    'facility': 'user',
    'address': '/dev/log',
}
LOGGING['loggers']['django.request']['handlers'] = ['mail_admins', 'console', 'syslog',]
LOGGING['loggers']['{{ project_name }}']['handlers'] = ['console', 'syslog',]

# Celery settings
BROKER_BACKEND = 'redis'
BROKER_URL = 'redis://%s/1' % env_setting('{{ project_name|upper }}_REDIS_SERVER')
CELERY_RESULT_BACKEND = 'redis://%s/2' % env_setting('{{ project_name|upper }}_REDIS_SERVER')
CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

# Email settings
