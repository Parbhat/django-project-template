# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module defines a set of common utilites used to manipulate datetimes

    :copyright: (c) 2015
"""
from __future__ import absolute_import
from contextlib import contextmanager
import datetime as dt
import logging
import time

from django.utils import timezone

LOGGER = logging.getLogger(__name__)


def now():
    """
    This function does not provide any additional functionality that the
    datetime module already provides, but because this method is written in
    python and not C, it can be mocked for testing purposes.
    """
    return timezone.now()


def today():
    """
    This function does not provide any additional functionality that the
    dateteim module already provides, but because this method is written in
    python and not C, it can be mocked for testing purposes.
    """
    return now().date()


@contextmanager
def measure_time(title, logger=None, level=logging.DEBUG):
    """
    This context manager logs out the amount of time elapsed while executing
    the context block.  If no logger is provided a default for this class is
    used.  The default logging level is DEBUG.
    """
    if logger is None:
        logger = LOGGER
    t1 = time.time()
    yield
    t2 = time.time()
    logger.log(level, '%s: %0.2f seconds elapsed' % (title, t2 - t1))


def datetime_to_epoch(value):
    "Convert a datetime object to epoch (seconds since 1970-1-1)"
    return int(time.mktime(value.timetuple()))


def epoch_to_datetime(value):
    "Convert epoch (seconds since 1970-1-1) to a datetime object"
    return dt.datetime.fromtimestamp(value)
