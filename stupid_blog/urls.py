# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from .views import PostDetailView, PostListView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='posts-latest'),
    url(r'^(?P<slug>\w[-\w]*)/$', PostDetailView.as_view(), name='post-detail'),
]