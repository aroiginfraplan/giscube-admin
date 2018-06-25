# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-21 12:32
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import layerserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('giscube', '0003_dbconnection'),
        ('layerserver', '0002_geojsonlayer_generated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geojsonlayer',
            name='data_file',
            field=models.FileField(blank=True, null=True, upload_to=layerserver.models.geojsonlayer_upload_path),
        ),
        migrations.AlterField(
            model_name='geojsonlayer',
            name='generated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geojsonlayer',
            name='last_fetch_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
