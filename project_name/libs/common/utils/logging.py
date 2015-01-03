# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.logging
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module defines a set of common utilites used for logging

    :copyright: (c) 2015
"""
from __future__ import absolute_import
from contextlib import contextmanager
import logging
import time


LOGGER = logging.getLogger(__name__)


@contextmanager
def disable_logging(level=logging.CRITICAL):
    logging.disable(level)
    yield
    logging.disable(logging.NOTSET)


@contextmanager
def timer(label, logger=None, level=logging.DEBUG, issue_print=False):
    logger = logger or LOGGER
    times = []
    start = time.time()
    yield
    times.append(time.time() - start)
    avg = sum(times) / len(times) if len(times) else 0
    msg = '%s took %0.3f seconds' % (label, avg)
    logger.log(level, msg)
    if issue_print:
        print(msg)
