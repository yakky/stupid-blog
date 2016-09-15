# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from parler.views import TranslatableSlugMixin, ViewUrlMixin


from .models import Post


class PostListView(ViewUrlMixin, ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'stupid_blog/post_list.html'
    # This is specific to parler - ViewUrlMixin requires ``view_url_name``
    # to be able to provide ``view.get_view_url``, which is mostly useful
    # when providing hreflang links in the header (who knows hreflang links?)
    view_url_name = 'posts-latest'

    def get_queryset(self):
        language = get_language()
        # This is the standard parler way to pick the ``correct`` languages
        # with takes fallback mechanism into account
        queryset = self.model._default_manager.active_translations(
            language_code=language
        )
        queryset = queryset.published()
        return queryset


# TranslatableSlugMixin is a parler magic mixin that automatically
# matches ``slug`` with ``translation__slug``
class PostDetailView(TranslatableSlugMixin, ViewUrlMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'stupid_blog/post_detail.html'
    # This is specific to parler - ViewUrlMixin requires ``view_url_name``
    # to be able to provide ``view.get_view_url``, which is mostly useful
    # when providing hreflang links in the header (who knows hreflang links?)
    view_url_name = 'posts-detail'

    def get_queryset(self):
        language = get_language()
        # This is the standard parler way to pick the ``correct`` languages
        # with takes fallback mechanism into account
        queryset = self.model._default_manager.active_translations(
            language_code=language
        )
        queryset = queryset.published()
        return queryset