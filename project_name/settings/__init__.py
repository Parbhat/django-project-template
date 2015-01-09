import os
import re
import warnings

from django.core.exceptions import ImproperlyConfigured


try:
    # Pulled from Honcho code with minor updates, reads local default
    # environment variables from a .env file located in the project root
    # directory by default, unless another env file is specified in
    # the ENV_FILE
    env_file = os.environ.get('ENV_FILE', '.env')
    with open(env_file, 'r') as f:
        for line in f:
            match = re.search(r'([A-Za-z_0-9]+)=(.*)$', line)
            if match:
                # if the value was wrapped in quotes strip them off
                key, val = match.group(1), match.group(2).strip('\'"')
                # only set the ENV variable if it has not already been defined
                os.environ.setdefault(key, val)
except IOError:
    pass


def env_setting(name, warn_user=True, fail_if_missing=False):
    value = os.environ.get(name)
    if value is None:
        if fail_if_missing:
            raise ImproperlyConfigured('%s has not been set' % name)
        if warn_user:
            warnings.warn('%s has not been set in your ENV' % name)
        return ''
    return value


def local_join(*path):
    """
    Convenience function for path joining
    """
    return os.path.join(os.path.dirname(__file__), *path)


class InvalidVarException(object):
    """
    Use this class to test for missing template variables.  Normally if a
    template variable can not be found, it will be replaced with a default
    value, typically the empty string.  By assigning the
    TEMPLATE_STRING_IF_INVALID setting to an instance of this class, an
    exception will be raised during the rendering process if missing.

    NOTE: you never want to use this in production
    """
    def __mod__(self, missing):
        try:
            missing_str = unicode(missing)
        except:
            missing_str = 'Failed to create string representation'
        raise Exception('Unknown template variable %r %s' % (missing, missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False
