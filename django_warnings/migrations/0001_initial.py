# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('subject', models.TextField()),
                ('message', models.TextField()),
                ('first_generated', models.DateTimeField()),
                ('last_generated', models.DateTimeField()),
                ('acknowledged', models.BooleanField(default=False)),
                ('last_acknowledger', models.PositiveIntegerField(default=None, null=True)),
                ('last_acknowledged', models.DateTimeField(default=None, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
