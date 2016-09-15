# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_apphooks_config.managers.parler import AppHookConfigTranslatableQueryset
from cms.models import PlaceholderField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from meta.models import ModelMeta
from parler.models import (
    TranslatableModel, TranslatedFields
)

from .cms_appconfig import BlogConfig
from .settings import get_setting


# This is not required, but it's always nicer to have a custom queryset
# when you deal with publish fields (or filtering fields in general)
# This new superclass it's just a convenient shortcut that adds ``namespace`` filtering
# method
class PostQueryset(AppHookConfigTranslatableQueryset):

    def published(self):
        return self.filter(publish=True, date_published__lte=now())

    def iacopos(self):
        return self.filter(author='iacopo')


# Do you know this Django 1.8 feature?
PostManager = PostQueryset.as_manager


@python_2_unicode_compatible
class Post(ModelMeta, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=1000),
        slug=models.SlugField(_('slug'), blank=True, default=''),
        abstract=HTMLField(_('abstract')),
    )
    image = FilerImageField(verbose_name=_('cover image'), null=True, on_delete=models.SET_NULL)
    publish = models.BooleanField(_('publish'), default=False)
    date_created = models.DateTimeField(_('created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('last modified'), auto_now=True)
    date_published = models.DateTimeField(_('published since'), default=timezone.now)
    app_config = AppHookConfigField(
        BlogConfig, null=True, verbose_name=_('app. config')
    )
    # when adding the placeholder field you have to save your models again
    # to make the placeholder field discoverable
    content = PlaceholderField('content')

    objects = PostManager()

    # _metadata maps known tags (as keys) to many different object types:
    #   * an attribute
    #   * a django field
    #   * a property
    #   * a callable (eventually accepting an argument)
    _metadata = {
        'title': 'title',
        'description': 'abstract_text',
        'og_description': 'abstract_text',
        'twitter_description': 'abstract_text',
        'gplus_description': 'abstract_text',
        'locale': 'get_locale',
        'image': 'get_image_full_url',
        'object_type': 'get_meta_attribute',
        'og_type': 'get_meta_attribute',
        'og_app_id': 'get_meta_attribute',
        'og_author_url': 'author',
        'twitter_type': 'get_meta_attribute',
        'twitter_site': 'get_meta_attribute',
        'twitter_author': 'author',
        'gplus_type': 'get_meta_attribute',
        'gplus_author': 'author',
        'published_time': 'date_published',
        'modified_time': 'date_modified',
        'url': 'get_absolute_url',
    }

    class Meta:
        verbose_name = _('blog article')
        verbose_name_plural = _('blog articles')
        ordering = ('-date_published', '-date_created')
        get_latest_by = 'date_published'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('%s:post-detail' % self.app_config.namespace, kwargs={'slug': self.safe_translation_getter('slug')})

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @property
    def abstract_text(self):
        # This is a property doing something on an attribute
        return strip_tags(self.abstract)

    def get_locale(self):
        # This a method without arguments
        return self.get_current_language()

    def get_meta_attribute(self, param):
        # This maps generic attributed in _metadata to settings. Is a callable accepting an argument
        # It's easy to create a generic method like this that picks data from different sources
        return get_setting(param.upper())

    def get_image_full_url(self):
        if self.image:
            return self.build_absolute_uri(self.image.url)
        return None

    def author(self):
        return get_setting('AUTHOR')