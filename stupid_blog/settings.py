# -*- coding: utf-8 -*-
from django.conf import settings


def get_setting(config):
    # This is a method that allows easier patching during tests as settings are not evaluated on import
    # but really at runtime
    defaults = {
        'PAGINATION': getattr(settings, 'STUPID_PAGINATION', 50)
    }
    return defaults[config]