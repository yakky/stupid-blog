# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(_('title'), max_length=1000)
    slug = models.SlugField(_('slug'))
    publish = models.BooleanField(_('publish'), default=False)
    abstract = HTMLField(_('abstract'))

    date_created = models.DateTimeField(_('created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('last modified'), auto_now=True)
    date_published = models.DateTimeField(_('published since'), default=timezone.now)

    class Meta:
        verbose_name = _('blog article')
        verbose_name_plural = _('blog articles')
        ordering = ('-date_published', '-date_created')
        get_latest_by = 'date_published'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
