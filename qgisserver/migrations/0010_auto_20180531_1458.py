# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-31 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qgisserver', '0009_auto_20180425_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='data',
            field=models.TextField(blank=True, null=True),
        ),
    ]