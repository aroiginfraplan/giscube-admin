# Generated by Django 2.2.11 on 2020-04-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layerserver', '0015_auto_20200115_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databaselayerfield',
            name='widget',
            field=models.CharField(choices=[('auto', 'Auto'), ('choices', 'Choices, one line per value'), ('creationdate', 'Creation date'), ('creationdatetime', 'Creation datetime'), ('creationuser', 'Creation user'), ('date', 'Date'), ('datetime', 'Date time'), ('distinctvalues', 'Distinct values'), ('foreignkey', 'Foreign key'), ('image', 'Image'), ('linkedfield', 'Linked Field'), ('modificationdate', 'Modification date'), ('modificationdatetime', 'Modification datetime'), ('modificationuser', 'Modification user'), ('sqlchoices', 'SQL choices')], default='auto', max_length=25, verbose_name='widget'),
        ),
    ]