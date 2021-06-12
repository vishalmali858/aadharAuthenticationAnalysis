# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-25 13:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fs', '0005_auto_20190225_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='us',
            name='user',
        ),
        migrations.AddField(
            model_name='us',
            name='password',
            field=models.CharField(default=datetime.datetime(2019, 2, 25, 13, 2, 1, 817907, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='us',
            name='username',
            field=models.CharField(default=datetime.datetime(2019, 2, 25, 13, 2, 10, 726983, tzinfo=utc), max_length=6),
            preserve_default=False,
        ),
    ]
