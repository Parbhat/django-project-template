# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.mixins
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains all model mixins that can be reused across apps

    :copyright: (c) 2015
"""
import base64
import json

from django.contrib.auth.hashers import PBKDF2PasswordHasher


class TokenModelMixin(object):
    """
    Any :class:`django.db.models.Model` extending this mixin will gain access
    to two methods.
    1) :method:`token` will generate an unique token for this particular model
    instance.
    2) :method:`verify` will check to see if the provided token is a match for
    this instance.
    """
    def unique_dict(self):
        """
        By default this method will just return a dict of the class fields
        mapped to string interpretations of their current values.  Override
        this method if the default implementation doesn't define a unique dict
        for the instance.
        """
        return dict([(f.name, f.value_to_string(self)) for f in self._meta.fields])

    def _key(self):
        class_key = '%s.%s' % (type(self).__module__, type(self).__name__)
        data = '%s-%s' % (class_key, json.dumps(self.unique_dict()))
        return base64.b64encode(json.dumps(data))

    def token(self):
        hasher = PBKDF2PasswordHasher()
        return hasher.encode(self._key(), hasher.salt())

    def verify(self, token):
        hasher = PBKDF2PasswordHasher()
        return hasher.verify(self._key(), token)
