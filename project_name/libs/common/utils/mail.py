# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.mail
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A collection of functions all pertainting to email

    :copyright: (c) 2015
"""
from __future__ import absolute_import
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import html2text
import premailer

LOGGER = logging.getLogger(__name__)


def send_html_email(subject, to, html=None, template=None, context=None,
        cc=None, bcc=None, from_email=None):
    """
    This generic HTML email sending function will before the following before
    sending:
        1) add site and static specific URLs to the template rendering context
        2) convert internal CSS to inline CSS
        3) convert the HTML to plain text for a normal body attachment
    """
    if html is None and template is None:
        raise TypeError('html or template is needed')
    if html is not None and template is not None:
        raise TypeError('only provide html or a template, not both')
    if isinstance(to, basestring):
        to = [to,]
    if isinstance(cc, basestring):
        cc = [cc,]
    if isinstance(bcc, basestring):
        bcc = [bcc,]
    if from_email is None or settings.DEBUG:
        from_email = settings.DEFAULT_FROM_EMAIL
    if template is not None:
        if context is None:
            context = {}
        context.update({
            'STATIC_URL': settings.STATIC_URL,
            'SITE_DOMAIN': settings.SITE_DOMAIN,
        })
        html = render_to_string(template, context)
    inline_html = premailer.transform(html)
    converter = html2text.HTML2Text()
    converter.ignore_images = True
    text = converter.handle(inline_html)
    msg = EmailMultiAlternatives(subject=subject, body=text,
            from_email=from_email, to=to, cc=cc, bcc=bcc)
    msg.attach_alternative(inline_html, 'text/html')
    LOGGER.info('sending email... [%s]' % msg.message().items())
    msg.send()
