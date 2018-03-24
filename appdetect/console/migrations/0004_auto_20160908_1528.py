# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-08 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0003_auto_20160623_0811'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Result',
            new_name='UserApps',
        ),
        migrations.AddField(
            model_name='apps',
            name='isDetect',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='apps',
            name='result',
            field=models.BooleanField(default=False),
        ),
    ]