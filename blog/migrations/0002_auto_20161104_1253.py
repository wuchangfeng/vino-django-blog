# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.DeleteModel(
            name='Nav',
        ),
        migrations.RemoveField(
            model_name='category',
            name='img',
        ),
    ]
