# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('downloaded', models.IntegerField(default=0)),
            ],
        ),
    ]
