# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-10 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamecollection', '0003_auto_20170809_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='img_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
