# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-24 12:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0006_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]