# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-03 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0010_auto_20170103_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='appFileName',
            field=models.CharField(default='none', max_length=50),
        ),
    ]