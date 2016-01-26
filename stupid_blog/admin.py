# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from stupid_blog.models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'publish', 'date_published')

admin.site.register(Post, PostAdmin)