# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-27 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0014_auto_20170111_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AddField(
            model_name='user',
            name='Email',
            field=models.EmailField(default='SOME STRING', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='passport',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='SOME STRING', max_length=50, primary_key=True, serialize=False),
        ),
    ]
