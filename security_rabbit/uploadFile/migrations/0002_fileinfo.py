# Generated by Django 2.1 on 2019-10-07 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadFile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.TextField(blank=True)),
                ('file_hash_sha1', models.CharField(max_length=40)),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('file_magic', models.CharField(blank=True, max_length=100, null=True)),
                ('file_state', models.IntegerField(blank=True, null=True)),
                ('peutils_packed', models.CharField(blank=True, max_length=200)),
                ('entropy', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('create_time', models.DateTimeField(blank=True)),
                ('modified_time', models.DateTimeField(blank=True)),
                ('accessed_time', models.DateTimeField(blank=True)),
                ('company', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=60)),
                ('product', models.CharField(blank=True, max_length=50)),
                ('prod_version', models.CharField(blank=True, max_length=40)),
                ('file_version', models.CharField(blank=True, max_length=40)),
                ('machine_type', models.CharField(blank=True, max_length=20)),
                ('signature_verification', models.CharField(max_length=100)),
                ('link_date', models.DateTimeField(blank=True)),
                ('signing_date', models.DateTimeField(blank=True)),
                ('signer', models.TextField(blank=True)),
                ('counter_signer', models.TextField(blank=True)),
                ('pe_machine', models.IntegerField(blank=True, null=True)),
                ('pe_sectionNum', models.IntegerField(blank=True, null=True)),
                ('pe_timeDateStamp', models.DateTimeField(blank=True)),
                ('pe_characteristics', models.IntegerField(blank=True, null=True)),
                ('pe_entryPoint', models.IntegerField(blank=True, null=True)),
                ('pe_sections', models.TextField(blank=True)),
                ('pe_imports', models.TextField(blank=True)),
                ('pe_exports', models.TextField(blank=True)),
                ('printablestr_txt', models.IntegerField(blank=True, null=True)),
                ('byte_distribution', models.TextField(blank=True)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]
