# Generated by Django 2.1 on 2019-11-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_remove_fileinfo_file_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='pe_timeDateStamp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]