# Generated by Django 4.2.1 on 2023-10-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApp', '0003_remove_logupload_uploadedfile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwarderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_data', models.TextField()),
                ('received_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DataEntry',
        ),
    ]