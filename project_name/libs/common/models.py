# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains all models that can be used across apps

    :copyright: (c) 2015
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils.text import slugify


class SlugModel(models.Model):
    """
    A base class for any model that wants to implement an auto generated slug
    field.
    """
    # how many times we'll retry creating a slug before giving up
    MAX_RETRIES = 100
    slug = models.SlugField(_('slug'), max_length=255, unique=True)

    class Meta:
        abstract = True

    @classmethod
    def is_valid_slug(cls, slug):
        """Convenience method to check if the given slug already exists."""
        return not cls.objects.filter(slug=slug).exists()

    @classmethod
    def get_by_slug(cls, slug):
        """
        Return the :class:`{{ project_name }}.libs.common.models.SlugModel` for the given
        slug.  If the slug dosen't exist, return None.

        :param slug: the slug value to search for
        """
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None

    def base_slug_value(self):
        """
        As a subclass of :class:`{{ project_name }}.libs.common.models.SlugModel` one must
        implement the :method:`{{ project_name }}.libs.common.models.SlugModel.base_slug_value`
        which returns a unicode value that is used as the basis of the slug value.
        """
        raise NotImplementedError

    def generate_slug(self, value=None):
        """
        Create a slug based on the value of
        :method:`{{ project_name }}.libs.common.models.SlugModel.base_slug_value`, ensure
        that the slug is unique by comparing it to existing slugs.
        """
        if value is None:
            value = self.base_slug_value()
        field = self._meta.get_field('slug')
        return slugify(value, max_length=field.max_length,
                usable=self.is_valid_slug, max_retries=self.MAX_RETRIES)

    def save(self, *args, **kwargs):
        """
        Right before a model is saved, check to see if the slug field has yet
        to be defined.  If so, generate and set the
        :attr:`{{ project_name }}.libs.common.models.SlugModel.slug`.
        """
        if not self.slug:
            # a slug has not yet been defined, generate one
            self.slug = self.generate_slug()
        return super(SlugModel, self).save(*args, **kwargs)
