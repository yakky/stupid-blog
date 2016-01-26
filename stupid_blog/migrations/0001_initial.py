# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('publish', models.BooleanField(default=False, verbose_name='publish')),
                ('abstract', djangocms_text_ckeditor.fields.HTMLField(verbose_name='abstract')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='published since')),
            ],
            options={
                'ordering': ('-date_published', '-date_created'),
                'get_latest_by': 'date_published',
                'verbose_name': 'blog article',
                'verbose_name_plural': 'blog articles',
            },
        ),
    ]
