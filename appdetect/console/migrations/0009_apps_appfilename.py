# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-03 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0008_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='apps',
            name='appFileName',
            field=models.CharField(default='no', max_length=50),
        ),
    ]
