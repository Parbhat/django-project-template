# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.views
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Collection of generic controller actions that are specific to the project

    :copyright: (c) 2015
"""
import logging
import socket

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError

from .utils.db import is_database_available, is_redis_available
from .utils.server import supervisor_process_states


logger = logging.getLogger(__name__)


def _supervisor_statuses():
    """
    Return all of the supervisor statuses, if a labels regex is passed in,
    only return those statuses whose labels match the regex.
    """
    statuses = {}
    for ip in settings.INTERNAL_IPS:
        try:
            for process, state in supervisor_process_states(ip, 9001).items():
                statuses['%s:%s' % (ip, process)] = state
        except AssertionError, e:
            return HttpResponseServerError(str(e))
        except socket.timeout:
            # Supervisor is not running on port 9001, so ignore the check
            pass
    return statuses


def verify(request):
    """
    Simple view to verify that the database and any other critical systems are
    up and running.  If everything is up and running return a 200 response,
    else return a 500.
    """
    if not is_database_available():
        return HttpResponseServerError('database is down')
    if not is_redis_available():
        return HttpResponseServerError('redis is down')
    for label, status in _supervisor_statuses().items():
        if status not in ['UP', 'RUNNING',]:
            return HttpResponseServerError('supervisor process %s is down' % label)
    return HttpResponse('ok')
