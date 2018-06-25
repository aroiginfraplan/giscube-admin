# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-21 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giscube', '0002_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engine', models.CharField(choices=[(b'django.contrib.gis.db.backends.postgis', b'Postgis')], max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('host', models.CharField(blank=True, max_length=100, null=True)),
                ('port', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'DBConnection',
                'verbose_name_plural': 'DBConnections',
            },
        ),
    ]