# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.admin import BaseAppHookConfig
from django.contrib import admin
from parler.admin import TranslatableAdmin

from stupid_blog.cms_appconfig import BlogConfig
from stupid_blog.models import Post


class PostAdmin(TranslatableAdmin):
    model = Post
    list_display = ('title', 'publish', 'date_published')
    date_hierarchy = 'date_published'

    def get_fieldsets(self, request, obj=None):
        # This is not required, but reminds that parler does not work with ``fieldsets`` attribute
        return (
            (None, {'fields': (
                'title', 'slug', 'publish', 'app_config',
                'date_published',
                'abstract'
            )}),
        )


# This is just a plain admin, but using django-appdata features
class BlogConfigAdmin(BaseAppHookConfig, TranslatableAdmin):

    # this is required due to a bug in django-appdata
    @property
    def declared_fieldsets(self):
        return self.get_fieldsets(None)

    def get_fieldsets(self, request, obj=None):
        """
        Fieldsets configuration
        """
        return [
            (None, {
                # config is the appdata json field
                # config.paginate_by is field contained in the ``config`` appdata container
                'fields': ('type', 'namespace', 'app_title', 'object_name', 'config.paginate_by')
            }),
        ]

admin.site.register(Post, PostAdmin)
admin.site.register(BlogConfig, BlogConfigAdmin)
