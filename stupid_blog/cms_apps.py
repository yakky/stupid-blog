# -*- coding: utf-8 -*-
from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_apphook_setup.base import AutoCMSAppMixin

from .settings import get_setting
from .cms_appconfig import BlogConfig


# This is the standard apphook class.
# Adding urls here will spare you from adding it in global urlconf
# and allows to dmove the application across the page tree
# Uses a different base class
# Adds the auto setup mixin
class StupidAppHook(AutoCMSAppMixin, CMSConfigApp):
    name = _('Blog')
    urls = ['stupid_blog.urls']
    app_name = 'djangocms_blog'
    app_config = BlogConfig
    # auto_setup contains configuration values
    # for auto creation of the missing items
    auto_setup = {
        'enabled': get_setting('AUTO_SETUP'),
        'home title': get_setting('AUTO_HOME_TITLE'),
        'page title': get_setting('AUTO_BLOG_TITLE'),
        'namespace': get_setting('AUTO_NAMESPACE'),
        'config_fields': {},
        'config_translated_fields': {
            'app_title': get_setting('AUTO_APP_TITLE'),
            'object_name': get_setting('DEFAULT_OBJECT_NAME')
        },
    }
apphook_pool.register(StupidAppHook)
# This is the call to the setup method
StupidAppHook.setup()