# -*- coding: utf-8 -*-
from django.db import models
from django.test import TestCase

from .models import SlugModel
from .mixins import TokenModelMixin
from .utils.text import slugify
from .utils.db import copy_model_instance

__all__ = ['SlugifyTests', 'SlugModelTests', 'TokenModelMixinTests',
    'CopyModelInstanceTests',]


class MockStorage(object):
    """
    helper class for testing slug conflicts
    """
    def __init__(self, data=None):
        self.data = data

    def is_unique(self, slug):
        if self.data is None:
            return True
        return slug not in self.data


class SlugifyTests(TestCase):
    def test_numbers_and_symbols(self):
        slug = slugify(' Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/')
        self.assertEqual('jack-jill-like-numbers-123-and-4-and-silly-characters', slug)
        slug = slugify(u' Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/')
        self.assertEqual('jack-jill-like-numbers-123-and-4-and-silly-characters', slug)

    def test_escaped_chars(self):
        slug = slugify(u"Un \xe9l\xe9phant \xe0 l\'or\xe9e du bois")
        self.assertEqual('un-elephant-a-loree-du-bois', slug)

    def test_hyphens(self):
        slug = slugify(u"how-to-handle existing hyphens")
        self.assertEqual('how-to-handle-existing-hyphens', slug)

    def test_underscores(self):
        slug = slugify(u"how_to_handle existing underscores")
        self.assertEqual('how-to-handle-existing-underscores', slug)

    def test_no_max_length(self):
        slug = slugify("set the max length of a slug", None)
        self.assertEqual('set-the-max-length-of-a-slug', slug)

    def test_max_length(self):
        slug = slugify("set the max length of a slug", 64)
        self.assertEqual('set-the-max-length-of-a-slug', slug)
        slug = slugify("set the max length of a slug", 18)
        self.assertEqual('set-the-max-length', slug)

    def test_conflict_under_max_len(self):
        storage = MockStorage(['this-is-a-slug', 'this-is-also-a-slug', 'this-is-also-a-slug~1'])
        self.assertEqual('this-is-a-slug~1', slugify('This is a slug', usable=storage.is_unique,))
        self.assertEqual('this-is-also-a-slug~2', slugify('This is also a slug', usable=storage.is_unique,))

    def test_conflict_over_max_len(self):
        slugs = ['over-the-l', 'multiple-d', 'multiple~1', 'multiple~2', 'multiple~3', 'multiple~4',
                   'multiple~5', 'multiple~6', 'multiple~7', 'multiple~8', 'multiple~9',
                   'single-digits-under-double-digits-over', 'single-digits-under-double-digits-over~1',
                   'single-digits-under-double-digits-over~2', 'single-digits-under-double-digits-over~3',
                   'single-digits-under-double-digits-over~4', 'single-digits-under-double-digits-over~5',
                   'single-digits-under-double-digits-over~6', 'single-digits-under-double-digits-over~7',
                   'single-digits-under-double-digits-over~8', 'single-digits-under-double-digits-over~9']
        storage = MockStorage(slugs)
        self.assertEqual('over-the~1', slugify('Over The Length', 10, storage.is_unique))
        self.assertEqual('multipl~10', slugify('Multiple Digits', 10, storage.is_unique))
        self.assertEqual('single-digits-under-double-digits-ove~10', slugify('Single Digits Under Double Digits Over', 40, storage.is_unique))

    def test_conflict_no_max_len(self):
        storage = MockStorage(['this-is-a-slug', 'this-is-also-a-slug', 'this-is-also-a-slug~1'])
        self.assertEqual('this-is-a-slug~1', slugify('This is a slug', None, usable=storage.is_unique,))
        self.assertEqual('this-is-also-a-slug~2', slugify('This is also a slug', None, usable=storage.is_unique,))

    def test_max_retries(self):
        storage = MockStorage(['slug', 'slug~1',])
        with self.assertRaises(RuntimeError):
            slugify('slug', max_length=None, usable=storage.is_unique, max_retries=1)


class SlugTestingModel(SlugModel):
    value = models.CharField(max_length=100)

    def base_slug_value(self):
        return unicode(self.value)


class SlugModelTests(TestCase):
    def test_is_valid_slug(self):
        self.assertTrue(SlugTestingModel.is_valid_slug('test'))
        SlugTestingModel.objects.create(value='test')
        self.assertFalse(SlugTestingModel.is_valid_slug('test'))

    def test_generate_slug(self):
        dummy = SlugTestingModel(value=u'Damir  Očko')
        self.assertEquals(dummy.generate_slug(), 'damir-ocko')
        SlugTestingModel.objects.create(value='Kurt Weber')
        dummy = SlugTestingModel(value='kurt weber')
        self.assertEquals(dummy.generate_slug(), 'kurt-weber~1')

    def test_get_by_slug(self):
        self.assertIsNone(SlugTestingModel.get_by_slug('test'))
        test = SlugTestingModel.objects.create(value='test')
        self.assertEquals(SlugTestingModel.get_by_slug('test'), test)


class TokenTestingModel(models.Model, TokenModelMixin):
    char = models.CharField(max_length=25)
    number = models.IntegerField()


class TokenTestingModel2(TokenTestingModel):
    pass


class TokenModelMixinTests(TestCase):
    def test_unique_dict(self):
        model = TokenTestingModel(char='a', number=2)
        self.assertEquals(model.unique_dict(), dict(id='None', char='a', number='2'))
        model = TokenTestingModel(id=10, char='t', number=2)
        self.assertEquals(model.unique_dict(), dict(id='10', char='t', number='2'))

    def test_invalid_token(self):
        model1 = TokenTestingModel(char='a')
        model2 = TokenTestingModel(char='b')
        self.assertFalse(model2.verify(model1.token()))

    def test_valid_token(self):
        model1 = TokenTestingModel(char='a')
        self.assertTrue(model1.verify(model1.token()))

    def test_invalid_token_class_mismatch(self):
        model1 = TokenTestingModel(char='a')
        model2 = TokenTestingModel2(char='a')
        self.assertFalse(model2.verify(model1.token()))


class CopyTestingModel(models.Model):
    char = models.CharField(max_length=15)
    number = models.IntegerField()
    boolean = models.BooleanField(default=False)


class CopyModelInstanceTests(TestCase):
    def test_unsaved_model(self):
        obj = CopyTestingModel(char='char', number=1, boolean=True)
        clone = copy_model_instance(obj)
        self.assertEquals(clone.char, 'char')
        self.assertEquals(clone.number, 1)
        self.assertEquals(clone.boolean, True)
        self.assertEquals(clone.pk, None)
        self.assertNotEquals(id(obj), id(clone))

    def test_saved_model(self):
        obj = CopyTestingModel.objects.create(char='char', number=1, boolean=True)
        clone = copy_model_instance(obj)
        clone.save()
        self.assertEquals(clone.char, 'char')
        self.assertEquals(clone.number, 1)
        self.assertEquals(clone.boolean, True)
        self.assertEquals(clone.pk, 2)
        self.assertNotEquals(obj, clone)
