# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.db
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A collection of functions all pertainting to database maniulation.

    :copyright: (c) 2015
"""
from __future__ import absolute_import

from django.db import connections
from django.db.models import AutoField

import redis


def is_database_available(alias='default'):
    """
    Return True if the database at the given alias is running, False if it
    doesn't exist or isn't running.
    """
    try:
        if alias not in connections:
            return False
        cursor = connections[alias].cursor()
        cursor.execute('SELECT 1')
        cursor.fetchone()
        return True
    except:
        return False


def is_redis_available(location='127.0.0.1:6379:0'):
    try:
        host, port, db = location.split(':')
        redis.Redis(host=host, port=port, db=db).ping()
        return True
    except:
        return False


def can_use_cache(manager):
    """
    Convenience function to test Django Many Related Managers to see if the
    relationship data has been cached using `prefetch_related`.  This is
    helpful as sometimes its much faster to perform a filter operation within
    python instead of on the DB, if the data is already cached.

    Return True if `manager.all()` will return a cached value, False otherwise
    """
    return manager.get_query_set()._prefetch_done


def copy_model_instance(obj):
    """
    Return a copy of the given model object.
    """
    initial = {}
    for f in obj._meta.fields:
        if not isinstance(f, AutoField) and f not in obj._meta.parents.values():
            initial[f.name] = getattr(obj, f.name)
    return obj.__class__(**initial)
