# Generated by Django 2.1 on 2019-10-18 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploadFile', '0006_auto_20191016_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileinfo',
            name='file_magic',
        ),
    ]
