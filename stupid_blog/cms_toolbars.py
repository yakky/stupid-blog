# -*- coding: utf-8 -*-

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.core.urlresolvers import reverse
from django.utils.translation import override, ugettext_lazy as _

from .settings import get_setting


@toolbar_pool.register
class BlogToolbar(CMSToolbar):

    def populate(self):
        if not self.is_current_app or not self.request.user.has_perm('stupid_blog.add_post'):
            return   # pragma: no cover
        admin_menu = self.toolbar.get_or_create_menu('stupid_blog', _('Blog'))
        with override(self.current_lang):
            # adds items to the toolbar
            # common ones:
            # - post list
            # - add post (maybe replace with the wizard)
            # - changeform of the namespace instance (eventually with permission checks)
            # - post changeform (eventually with permission checks)
            url = reverse('admin:stupid_blog_post_changelist')
            admin_menu.add_modal_item(_('Post list'), url=url)
            url = reverse('admin:stupid_blog_post_add')
            admin_menu.add_modal_item(_('Add post'), url=url)
            # This is a variable set by the view which allows to retrieve the current state of the view
            current_config = getattr(self.request, get_setting('CURRENT_NAMESPACE'), None)
            if current_config:
                url = reverse('admin:stupid_blog_blogconfig_change', args=(current_config.pk,))
                admin_menu.add_modal_item(_('Edit configuration'), url=url)

            # This is a variable set by the view which allows to retrieve the current post
            current_post = getattr(self.request, get_setting('CURRENT_POST_IDENTIFIER'), None)
            if current_post and self.request.user.has_perm('stupid_blog.change_post'):  # pragma: no cover  # NOQA
                admin_menu.add_modal_item(_('Edit Post'), reverse(
                    'admin:stupid_blog_post_change', args=(current_post.pk,)),
                    active=True)

    def add_publish_button(self):
        """
        Adds the publish button to the toolbar if the current post is unpublished
        """
        current_post = getattr(self.request, get_setting('CURRENT_POST_IDENTIFIER'), None)
        if (self.toolbar.edit_mode and current_post and
                not current_post.publish and
                self.request.user.has_perm('stupid_blog.change_post')
            ):  # pragma: no cover  # NOQA
            classes = ['cms-btn-action', 'blog-publish']
            title = _('Publish {0} now').format(current_post.app_config.object_name)

            url = admin_reverse('stupid_blog_publish_article', args=(current_post.pk,))

            self.toolbar.add_button(title, url=url, extra_classes=classes, side=self.toolbar.RIGHT)

    def post_template_populate(self):
        current_post = getattr(self.request, get_setting('CURRENT_POST_IDENTIFIER'), None)
        if current_post and self.request.user.has_perm('stupid_blog.change_post'):  # pragma: no cover  # NOQA
            self.add_publish_button()