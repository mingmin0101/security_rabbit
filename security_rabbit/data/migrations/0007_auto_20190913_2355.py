# Generated by Django 2.1 on 2019-09-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20190913_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='counter_signer',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_magic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_path',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='pe_exports',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='pe_imports',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='pe_sections',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='signer',
            field=models.TextField(blank=True),
        ),
    ]
