# -*- coding: utf-8 -*-
from django.conf import settings


def get_setting(config):
    # This is a method that allows easier patching during tests as settings are not evaluated on import
    # but really at runtime
    defaults = {
        'PAGINATION': getattr(settings, 'STUPID_PAGINATION', 50),
        'AUTO_SETUP': getattr(settings, 'STUPID_AUTO_SETUP', True),
        'AUTO_HOME_TITLE': getattr(settings, 'STUPID_AUTO_HOME_TITLE', 'Home'),
        'AUTO_BLOG_TITLE': getattr(settings, 'STUPID_AUTO_BLOG_TITLE', 'Blog'),
        'AUTO_NAMESPACE': getattr(settings, 'STUPID_AUTO_NAMESPACE', 'blog'),
        'AUTO_APP_TITLE': getattr(settings, 'STUPID_AUTO_APP_TITLE', 'Blog'),
        'DEFAULT_OBJECT_NAME': getattr(settings, 'STUPID_DEFAULT_OBJECT_NAME', 'Post'),
    }
    return defaults[config]