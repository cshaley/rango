# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20160311_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
