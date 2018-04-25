# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-25 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import qgisserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('qgisserver', '0008_auto_20180423_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='wms_buffer_enabled',
            field=models.BooleanField(default=False, verbose_name=b'buffer enabled'),
        ),
        migrations.AddField(
            model_name='service',
            name='wms_buffer_size',
            field=models.CharField(blank=True, help_text=b'Buffer around tiles, e.g. 64,64', max_length=12, null=True, validators=[qgisserver.models.validate_integer_pair], verbose_name=b'buffer size'),
        ),
        migrations.AddField(
            model_name='service',
            name='wms_tile_sizes',
            field=models.TextField(blank=True, help_text=b'Integer pairs in different lines e.g.<br/>256,256<br/>512,512', null=True, validators=[qgisserver.models.validate_integer_pair_list], verbose_name=b'tile sizes'),
        ),
    ]
