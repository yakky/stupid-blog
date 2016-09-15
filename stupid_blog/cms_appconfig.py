# -*- coding: utf-8 -*-
from aldryn_apphooks_config.models import AppHookConfig
from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


# This is a plain model with inherited (from AppHookConfig) appdata field
class BlogConfig(TranslatableModel, AppHookConfig):
    """
    Adds some translatable, per-app-instance fields.
    """
    # You can add as many fields you want
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
        object_name=models.CharField(
            _('object name'), max_length=234, default=_('article')
        ),
    )

    class Meta:
        verbose_name = _('blog config')
        verbose_name_plural = _('blog configs')

    def get_app_title(self):
        return getattr(self, 'app_title', _('untitled'))


# The appdata form allows to define as many fields you want without any shema migration
# Handy when you are iterating quickly and you want to add non-structural information
# to your application
# The fields of this form are contained in the ``BlogConfig.config`` field
# Thanks to AppHookConfig they can be accessed directly from the ``BlogConfig`` class instance
# e.g: post.app_config.paginate_by
class BlogConfigForm(AppDataForm):
    paginate_by = forms.IntegerField(
        label=_('Paginate size'), required=False, initial=50,
        help_text=_('When paginating list views, how many articles per page?')
    )
setup_config(BlogConfigForm, BlogConfig)
