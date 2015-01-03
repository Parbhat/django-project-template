# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.middleware
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains middleware that is common to {{ project_name }}

    :copyright: (c) 2015
"""


class PjaxMiddleware(object):
    """
    If the request was made via PJAX, add the original request path to the
    response.
    """
    def process_response(self, request, response):
        if 'HTTP_X_PJAX' in request.META:
            response['X-PJAX-URL'] = request.path
        return response
