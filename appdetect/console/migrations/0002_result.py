# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDetect', models.IntegerField(default=0)),
                ('result', models.BooleanField()),
                ('apps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='console.Apps')),
            ],
        ),
    ]
