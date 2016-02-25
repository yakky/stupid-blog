# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import PostDetailView, PostListView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='posts-latest'),
    # URLs can be translated as well
    url(_(r'^post/(?P<slug>[\w-]+)/$'), PostDetailView.as_view(), name='post-detail'),
]