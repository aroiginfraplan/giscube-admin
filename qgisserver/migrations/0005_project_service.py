# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-10 10:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qgisserver', '0004_auto_20180410_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qgisserver.Service'),
        ),
    ]