# -*- coding: utf-8 -*-
from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .cms_appconfig import BlogConfig


# This is the standard apphook class.
# Adding urls here will spare you from adding it in global urlconf
# and allows to dmove the application across the page tree
# Uses a different base class
class StupidAppHook(CMSConfigApp):
    name = _('Blog')
    urls = ['stupid_blog.urls']
    app_name = 'djangocms_blog'
    app_config = BlogConfig
apphook_pool.register(StupidAppHook)
