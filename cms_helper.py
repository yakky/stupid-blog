#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from tempfile import mkdtemp


def gettext(s): return s

HELPER_SETTINGS = dict(
    ROOT_URLCONF='tests.test_utils.urls',
    INSTALLED_APPS=[
        'filer',
        'parler',
        'easy_thumbnails',
        'djangocms_text_ckeditor',
        'cmsplugin_filer_image',
        'tests.test_utils',
    ],
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', gettext('English')),
        ('fr', gettext('French')),
        ('it', gettext('Italiano')),
    ),
    CMS_LANGUAGES={
        1: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
            {
                'code': 'it',
                'name': gettext('Italiano'),
                'public': True,
            },
            {
                'code': 'fr',
                'name': gettext('French'),
                'public': True,
            },
        ],
        2: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
        ],
        'default': {
            'hide_untranslated': False,
        },
    },
    CMS_TEMPLATES=(
        ('blog.html', 'Blog template'),
    ),
    THUMBNAIL_PROCESSORS=(
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    SITE_ID=1,
)


def run():
    from djangocms_helper import runner
    runner.cms('stupid_blog')

if __name__ == '__main__':
    run()
