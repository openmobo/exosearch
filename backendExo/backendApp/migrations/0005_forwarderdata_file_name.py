# Generated by Django 4.2.1 on 2023-10-23 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApp', '0004_forwarderdata_delete_dataentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='forwarderdata',
            name='file_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]