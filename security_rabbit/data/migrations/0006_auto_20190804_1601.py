# Generated by Django 2.1 on 2019-08-04 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20190804_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanningrecord',
            name='advance_option',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scanningrecord',
            name='customized_option',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scanningrecord',
            name='normal_option',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
