# Generated by Django 4.2.1 on 2023-10-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApp', '0005_forwarderdata_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='forwarderdata',
            name='new_data',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
