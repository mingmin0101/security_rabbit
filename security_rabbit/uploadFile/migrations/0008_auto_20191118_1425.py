# Generated by Django 2.1 on 2019-11-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadFile', '0007_remove_fileinfo_file_magic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileinfo',
            name='byte_distribution',
        ),
        migrations.RemoveField(
            model_name='fileinfo',
            name='printablestr_txt',
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='exec_ability',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='network_ability',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='rw_ability',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]