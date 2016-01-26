# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.utils.timezone import now
from django.views.generic import DetailView, ListView


from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'stupid_blog/post_list.html'

    def get_queryset(self):
        return super(PostListView, self).get_queryset().filter(
                publish=True, date_published__lte=now()
        )


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'stupid_blog/post_detail.html'

    def get_queryset(self):
        return super(PostDetailView, self).get_queryset().filter(
                publish=True, date_published__lte=now()
        )
