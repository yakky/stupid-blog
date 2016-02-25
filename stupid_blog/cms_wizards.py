# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.utils.permissions import get_current_user

try:
    from cms.wizards.wizard_base import Wizard
    from cms.wizards.wizard_pool import wizard_pool
    from django import forms
    from django.utils.text import slugify
    from django.utils.translation import ugettext_lazy as _
    from parler.forms import TranslatableModelForm

    from .cms_appconfig import BlogConfig
    from .models import Post

    # Model form which defines the "essential" fields
    # Must contains all the required fields without defaults
    # Suggested to create one form for each apphook config instance
    # to let users pick the "right" object to creare fro the very start
    # But you must correctly inizialize it in the form init
    # In the save method you can further customize how the models are created
    # See https://github.com/divio/django-cms/blob/develop/cms/forms/wizards.py#L150
    class PostWizardForm(TranslatableModelForm):
        default_appconfig = None

        def __init__(self, *args, **kwargs):
            if 'initial' not in kwargs or not kwargs.get('initial', False):
                kwargs['initial'] = {}
            kwargs['initial']['app_config'] = self.default_appconfig
            if 'data' in kwargs and kwargs['data'] is not None:
                kwargs['data']['1-app_config'] = self.default_appconfig
            super(PostWizardForm, self).__init__(*args, **kwargs)
            self.fields['app_config'].widget = forms.Select(
                attrs=self.fields['app_config'].widget.attrs,
                choices=self.fields['app_config'].widget.choices,
            )
            self.fields['app_config'].widget.attrs['disabled'] = True

        class Meta:
            model = Post
            fields = ['app_config', 'title', 'abstract']

        class Media:
            js = ('admin/js/jquery.js', 'admin/js/jquery.init.js',)


    class PostWizard(Wizard):
        pass

    # This allows to create the actual per-apphook instance forms
    for config in BlogConfig.objects.all().order_by('namespace'):
        new_wizard = type(str(slugify(config.app_title)), (PostWizard,), {})
        new_form = type(str('{0}Form').format(slugify(config.app_title)), (PostWizardForm,), {
            'default_appconfig': config.pk
        })
        post_wizard = new_wizard(
            title=_('New {0}').format(config.object_name),
            weight=200,
            form=new_form,
            model=Post,
            description=_('Create a new {0} in {1}').format(config.object_name, config.app_title),
        )
        wizard_pool.register(post_wizard)
except ImportError:
    # For django CMS version not supporting wizards just ignore this file
    pass