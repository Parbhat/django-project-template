# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.text
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A collection of functions all pertainting to text maniulation

    :copyright: (c) 2015
"""
from django.utils.text import slugify as django_slugify

from unidecode import unidecode


def slugify(value, max_length=128, usable=None, max_retries=1000):
    """
    Normalizes string, removing non-ascii characters, converts to lowercase,
    converts underscores and spaces to hyphens, removes all other non-alphanumeric
    characters.

    Providing an exists function will result in conflict resolution. Conflicts
    will have a suffix appended to indicate the index. e.g. samsung, samsung~1
    ... samsung~10

    If the appending the suffix exceeds maxlen then the original slug will be
    truncated to fit exactly maxlen. e.g. samsung, samsun~1, samsun~2 ... samsu~10

    The usable function takes a single value `slug` and returns True or False.
    The algorithm will continue to try new slugs, until the usable method
    returns True.

    To prevent an infinate loop condition, the max_retries variable limits how
    many different slugs to try before raising a RuntimeError.

        def valid_slug(self, slug):
            parent = self.parent or self.parent_id
            return not MyModel.objects.filter(parent=parent, slug=slug).exists()

        def save(self, *args, **kwargs):
            if not self.slug is None and self.name:
                self.slug = slugify(self.name, exists=self.valid_slug)

    :param value: string to normalize
    :param maxlen: maximum length for string, default is 128. If evaluates
        False then no max length will be enforced
    :param exists: a function that returns True if the slug already exists,
        False otherwise.
    :param max_retries: limit the number of times to retry slug creation
        before giving up.
    :return: slugified value
    """
    if usable and not callable(usable):
        raise TypeError('usable argument must be a callable')

    if isinstance(value, unicode):
        # if the value is currently unicode, convert it back to a ascii
        # traslating any special chars to similar ones in ascii.
        # For example: unidecode(u'Očko') -> 'Ocko'
        value = unidecode(value)
    slug = django_slugify(unicode(value)).replace('_', '-')

    if max_length:
        slug = slug[:max_length]

    # decide whether to resolve conflicts
    if usable is None:
        return slug

    # conflict detection/resolution
    copy = slug
    count = 0
    # TODO: need a better slug collision algorithm, as this can be expensive
    while not usable(slug):
        count += 1
        if max_retries and count > max_retries:
            raise RuntimeError('slugify surpassed its max_retries limit of %s'
                    % max_retries)
        suffix = '~%d' % count
        slug = copy[:max_length - len(suffix)] if max_length else copy
        slug = '%s%s' % (slug, suffix)
    return slug
