# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.mixins import AppConfigMixin
from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from parler.views import TranslatableSlugMixin, ViewUrlMixin

from .models import Post
from .settings import get_setting


class PostListView(AppConfigMixin, ViewUrlMixin, ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'stupid_blog/post_list.html'
    # This is specific to parler - ViewUrlMixin requires ``view_url_name``
    # to be able to provide ``view.get_view_url``, which is mostly useful
    # when providing hreflang links in the header (who knows hreflang links?)
    view_url_name = 'posts-latest'

    def get_queryset(self):
        language = get_language()
        # We need to start filtering on namespace to pick the 'right' models
        queryset = self.model._default_manager.namespace(
            self.namespace
        # This is the standard parler way to pick the ``correct`` languages
        # with takes fallback mechanism into account
        ).active_translations(
            language_code=language
        )
        queryset = queryset.published()
        # This allows to communicate to the toolbar the current namespace
        setattr(self.request, get_setting('CURRENT_NAMESPACE'), self.config)
        return queryset

    def get_paginate_by(self, queryset):
        # self.config is added automatically by AppConfigMixin and points to the BlogConfig
        # instance
        return self.config.paginate_by or get_setting('PAGINATION')


# TranslatableSlugMixin is a parler magic mixin that automatically
# matches ``slug`` with ``translation__slug``
# AppConfigMixin handles the namespace magic
class PostDetailView(AppConfigMixin, TranslatableSlugMixin, ViewUrlMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'stupid_blog/post_detail.html'
    # This is specific to parler - ViewUrlMixin requires ``view_url_name``
    # to be able to provide ``view.get_view_url``, which is mostly useful
    # when providing hreflang links in the header (who knows hreflang links?)
    view_url_name = 'posts-detail'

    def get_queryset(self):
        language = get_language()
        # We need to start filtering on namespace to pick the 'right' models
        queryset = self.model._default_manager.namespace(
            self.namespace
        # This is the standard parler way to pick the ``correct`` languages
        # with takes fallback mechanism into account
        ).active_translations(
            language_code=language
        )
        queryset = queryset.published()
        # This allows to communicate to the toolbar the current namespace
        setattr(self.request, get_setting('CURRENT_NAMESPACE'), self.config)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # This allows to communicate to the toolbar the opened post
        setattr(self.request, get_setting('CURRENT_POST_IDENTIFIER'), self.get_object())
        return context