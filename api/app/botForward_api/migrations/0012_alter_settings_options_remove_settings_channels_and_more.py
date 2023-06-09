# Generated by Django 4.2 on 2023-05-04 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botForward_api', '0011_channel_alter_media_file_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Настройки', 'verbose_name_plural': 'Настройки'},
        ),
        migrations.RemoveField(
            model_name='settings',
            name='channels',
        ),
        migrations.AddField(
            model_name='channel',
            name='settings',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.DO_NOTHING, related_name='channels', to='botForward_api.settings'),
            preserve_default=False,
        ),
    ]
