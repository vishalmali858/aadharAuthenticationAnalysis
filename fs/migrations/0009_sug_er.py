# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-13 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fs', '0008_sug'),
    ]

    operations = [
        migrations.AddField(
            model_name='sug',
            name='ER',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
