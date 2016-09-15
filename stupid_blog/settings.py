# -*- coding: utf-8 -*-
from django.conf import settings


def get_setting(config):
    # This is a method that allows easier patching during tests as settings are not evaluated on import
    # but really at runtime
    defaults = {
        'AUTHOR': getattr(settings, 'AUTHOR', 'Me'),
        'PAGINATION': getattr(settings, 'STUPID_PAGINATION', 50),
        'AUTO_SETUP': getattr(settings, 'STUPID_AUTO_SETUP', True),
        'AUTO_HOME_TITLE': getattr(settings, 'STUPID_AUTO_HOME_TITLE', 'Home'),
        'AUTO_BLOG_TITLE': getattr(settings, 'STUPID_AUTO_BLOG_TITLE', 'Blog'),
        'AUTO_NAMESPACE': getattr(settings, 'STUPID_AUTO_NAMESPACE', 'blog'),
        'AUTO_APP_TITLE': getattr(settings, 'STUPID_AUTO_APP_TITLE', 'Blog'),
        'DEFAULT_OBJECT_NAME': getattr(settings, 'STUPID_DEFAULT_OBJECT_NAME', 'Post'),
        'CURRENT_POST_IDENTIFIER': getattr(settings, 'STUPID_CURRENT_POST_IDENTIFIER', 'stupid_post_current_post'),
        'CURRENT_NAMESPACE': getattr(settings, 'STUPID_CURRENT_NAMESPACE', 'stupid_post_current_config'),
        'OG_APP_ID': getattr(settings, 'STUPID_OG_APP_ID', '123456789'),
        'OG_TYPE': getattr(settings, 'STUPID_OG_TYPE', 'Page'),
        'OBJECT_TYPE': getattr(settings, 'STUPID_OBJECT_TYPE', 'Page'),
        'TWITTER_TYPE': getattr(settings, 'STUPID_TWITTER_TYPE', 'Summary'),
        'TWITTER_SITE': getattr(settings, 'STUPID_TWITTER_SITE', '@Example'),
        'GPLUS_TYPE': getattr(settings, 'STUPID_GPLUS_TYPE', 'Article'),
    }
    return defaults[config]