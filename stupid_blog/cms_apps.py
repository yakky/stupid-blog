# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


# This is the standard apphook class.
# Adding urls here will spare you from adding it in global urlconf
# and allows to dmove the application across the page tree
class StupidAppHook(CMSApp):
    name = _('Blog')
    urls = ['stupid_blog.urls']
apphook_pool.register(StupidAppHook)
