from __future__ import absolute_import
import os

# import the settings here to preload the ENV settings
from . import settings as proj_settings

from django.conf import settings

from celery import Celery

try:
    # if available, initialize the newrelic environment
    import newrelic.agent

    config_file = os.environ.get('NEW_RELIC_CONFIG_FILE')
    environment = os.environ.get('NEW_RELIC_ENVIRONMENT')

    newrelic.agent.initialize(config_file, environment)
except ImportError:
    pass

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings.dev')

app = Celery('{{ project_name }}')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
