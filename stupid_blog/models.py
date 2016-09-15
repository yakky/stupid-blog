# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_apphooks_config.managers.parler import AppHookConfigTranslatableQueryset
from cms.models import PlaceholderField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from parler.models import (
    TranslatableModel, TranslatedFields
)

from stupid_blog.cms_appconfig import BlogConfig


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
class Post(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=1000),
        slug=models.SlugField(_('slug'), blank=True, default=''),
        abstract=HTMLField(_('abstract')),
    )
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
