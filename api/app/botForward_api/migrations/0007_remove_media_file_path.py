# Generated by Django 4.2 on 2023-04-28 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botForward_api', '0006_media_file_path_alter_media_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='file_path',
        ),
    ]