# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from parler.admin import TranslatableAdmin

from stupid_blog.models import Post


class PostAdmin(TranslatableAdmin):
    model = Post
    list_display = ('title', 'publish', 'date_published')
    date_hierarchy = 'date_published'

    def get_fieldsets(self, request, obj=None):
        # This is not required, but reminds that parler does not work with ``fieldsets`` attribute
        return (
            (None, {'fields': (
                'title', 'slug', 'publish',
                'date_published',
                'abstract'
            )}),
        )

admin.site.register(Post, PostAdmin)
