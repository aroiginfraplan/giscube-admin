# Generated by Django 2.1.7 on 2019-05-07 09:14

from django.db import migrations, models
import qgisserver.utils


class Migration(migrations.Migration):

    dependencies = [
        ('qgisserver', '0014_service_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AlterField(
            model_name='project',
            name='data',
            field=models.TextField(blank=True, null=True, verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=True, help_text='Enable/disable usage', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='keywords',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='keywords'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='project_file',
            field=models.FileField(upload_to=qgisserver.utils.unique_service_directory, verbose_name='project file'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_path',
            field=models.CharField(max_length=255, verbose_name='service path'),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='service',
            name='visibility',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='private', help_text="visibility='Private' restricts usage to authenticated users", max_length=10, verbose_name='visibility'),
        ),
        migrations.AlterField(
            model_name='service',
            name='visible_on_geoportal',
            field=models.BooleanField(default=False, verbose_name='visible on geoportal'),
        ),
    ]
