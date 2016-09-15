# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.admin import BaseAppHookConfig
from cms.admin.placeholderadmin import FrontendEditableAdminMixin, PlaceholderAdminMixin
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language_from_request
from parler.admin import TranslatableAdmin

from stupid_blog.cms_appconfig import BlogConfig
from stupid_blog.models import Post


# Add FrontendEditableAdminMixin
class PostAdmin(FrontendEditableAdminMixin, PlaceholderAdminMixin, TranslatableAdmin):
    model = Post
    list_display = ('title', 'publish', 'date_published')
    date_hierarchy = 'date_published'
    # declare the fields you want editable by render_model
    frontend_editable_fields = ('title', 'abstract')

    def get_fieldsets(self, request, obj=None):
        # This is not required, but reminds that parler does not work with ``fieldsets`` attribute
        return (
            (None, {'fields': (
                'title', 'slug', 'publish', 'app_config',
                'date_published',
                'abstract'
            )}),
        )

    def get_urls(self):
        """
        Customize the modeladmin urls
        """
        urls = [
            url(r'^publish/([0-9]+)/$', self.admin_site.admin_view(self.publish_post),
                name='stupid_blog_publish_article'),
        ]
        urls.extend(super(PostAdmin, self).get_urls())
        return urls

    # This method allows to publish posts with a remote call.
    # In reality you will want to do security checks here
    # (user permissions, use POSTs etc)
    def publish_post(self, request, pk):
        """
        Admin view to publish a single post
        :param request: request
        :param pk: primary key of the post to publish
        :return: Redirect to the post itself (if found) or fallback urls
        """
        language = get_language_from_request(request, check_path=True)
        try:
            post = Post.objects.get(pk=int(pk))
            post.publish = True
            post.save()
            return HttpResponseRedirect(post.get_absolute_url(language))
        except Exception:
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect(reverse('stupid_blog:posts-latest'))


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
