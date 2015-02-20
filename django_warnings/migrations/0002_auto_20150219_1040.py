# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_warnings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warning',
            name='identifier',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='warning',
            name='url_params',
            field=json_field.fields.JSONField(default='null', help_text=b'An object with keys that help the frontend form a url', null=True, blank=True),
            preserve_default=True,
        ),
    ]
