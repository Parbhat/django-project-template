"""
WSGI config for {{ projcet_name }} project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
# import the settings here to preload the ENV settings
import settings

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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings.development')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
