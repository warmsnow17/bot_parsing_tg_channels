import os

from django.db import models
from django.utils.safestring import SafeString
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from pyrogram import Client
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
from django.conf import settings
from pyrogram.types import InputMediaPhoto, InputMediaVideo

load_dotenv()


class Channel(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='ID канала')
    name = models.CharField(max_length=300, verbose_name='Имя канала',
                            null=True, blank=True)
    settings = models.ForeignKey("Settings", related_name='channels',
                                 on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name if self.name else self.telegram_id


class Settings(models.Model):
    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    forwarding = models.BooleanField(default=False)


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.text if self.text else 'Пост без текста'


class Media(models.Model):
    file = models.FileField(upload_to='', null=True, blank=True)
    post = models.ForeignKey(Post,
                             related_name='media', on_delete=models.CASCADE)

    def __str__(self):
        link = f'<a href="{self.file.url}">Открыть</a>'
        return SafeString(link) if self.file.url else 'No Media'


def get_media_type(file_name):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'image'
    elif file_name.lower().endswith(('.mp4', '.mkv')):
        return 'video'
    else:
        return None


async def send_message(text, media_list):
    async with Client('djangoclient',
                      os.getenv('API_ID'), os.getenv('API_HASH')) as client:
        if len(media_list) > 1:
            input_files = []
            for i, media in enumerate(media_list):
                if get_media_type(media) == 'image':
                    if i == 0:
                        input_files.append(
                            InputMediaPhoto(f'{settings.MEDIA_ROOT}/{media}',
                                            caption=text))
                    else:
                        input_files.append(
                            InputMediaPhoto(f'{settings.MEDIA_ROOT}/{media}'))
                elif get_media_type(media) == 'video':
                    input_files.append(
                        InputMediaVideo(f'{settings.MEDIA_ROOT}/{media}'))
            await client.send_media_group(int(os.getenv('CHANNEL_3')), input_files)
        elif len(media_list) == 1:
            if get_media_type(media_list[0]) == 'image':
                await client.send_photo(
                    int(os.getenv('CHANNEL_3')),
                    f'{settings.MEDIA_ROOT}/{media_list[0]}',
                    text)
            elif get_media_type(media_list[0]) == 'video':
                await client.send_video(
                    int(os.getenv('CHANNEL_3')),
                    f'{settings.MEDIA_ROOT}/{media_list[0]}',
                    text)
        else:
            await client.send_message(int(os.getenv('CHANNEL_3')), text)


@receiver(post_save, sender=Post)
def post_verified(sender, instance, update_fields, **kwargs):
    if instance.is_verified:
        medias = instance.media.all()
        media_list = [media.file.name for media in medias]
        text = instance.text
        sync_send_message = async_to_sync(send_message)
        sync_send_message(text=text, media_list=media_list)

        for media in media_list:
            os.remove(f'{settings.MEDIA_ROOT}/{media}')
        Media.objects.filter(post=instance).delete()

