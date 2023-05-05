import os
import sys
from dotenv import load_dotenv
from config import client
from interface import interface
from loguru import logger
from pyrogram import types, filters, Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from django.conf import settings
import django
import os
sys.path.append(os.path.abspath('/app/api/app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
from botForward_api.models import Settings


load_dotenv()

media_group_chats = set()


def send_to_channel(client: Client, message: types.Message, media_group=False):
    target_channel = int(os.getenv('CHANNEL_3'))
    if media_group:
        media_group_messages = client.get_media_group(chat_id=message.chat.id, message_id=message.id)
        media_list = []
        for media in media_group_messages:
            if media.photo:
                if media.caption:
                    media_list.append(InputMediaPhoto(media.photo.file_id, caption=media.caption.markdown))
                else:
                    media_list.append(InputMediaPhoto(media.photo.file_id))
            elif media.video:
                if media.caption:
                    media_list.append(InputMediaVideo(media.video.file_id, caption=media.caption.markdown))
                else:
                    media_list.append(InputMediaVideo(media.video.file_id))
        client.send_media_group(chat_id=target_channel, media=media_list)
    else:
        if message.photo:
            client.send_photo(chat_id=target_channel, photo=message.photo.file_id, caption=message.caption.markdown)
        elif message.video:
            client.send_video(chat_id=target_channel, video=message.video.file_id, caption=message.caption.markdown)
        else:
            client.send_message(chat_id=target_channel, text=message.text.markdown)


@client.on_message(filters=(filters.channel) & ~(filters.media_group))
def post_handler(client: Client, message: types.Message):
    config = Settings.objects.first()
    if not config:
        return

    channels = [channel.telegram_id for channel in config.channels.all()]
    # for channel in channels:
    #     client.join_chat(channel)
    if message.chat.id not in channels:
        return

    if config.forwarding:
        send_to_channel(client, message)
    else:
        files = []
        if message.photo or message.video:
            media = client.download_media(message, f'{settings.MEDIA_ROOT}/')
            files.append(media)
        text = message.caption.markdown if message.caption else message.text.markdown
        data = {'text': text,
                'media': files
                }
        logger.warning(data)
        if interface.send_post(data=data):
            logger.warning('Успех')
        else:
            logger.warning('Провал')


@client.on_message(filters=[filters.channel, filters.media_group])
def media_group_handler(client: Client, message: types.Message):
    config = Settings.objects.first()
    if not config:
        return
    logger.warning(config.channels)
    channels = [channel.telegram_id for channel in config.channels.all()]
    # for channel in channels:
    #     client.join_chat(channel)
    logger.warning(channels)
    if message.chat.id not in channels:
        return

    if message.chat.id in media_group_chats:
        logger.warning('Kek')
        return

    media_group_chats.add(message.chat.id)

    if config.forwarding:
        send_to_channel(client, message, media_group=True)
    else:
        media_group_messages = client.get_media_group(chat_id=message.chat.id, message_id=message.id)
        files = []
        text = None
        for media_message in media_group_messages:
            media = client.download_media(media_message, f'{settings.MEDIA_ROOT}/')
            files.append(media)
            if media_message.caption:
                text = media_message.caption.markdown

        data = {'text': text,
                'media': files
                }
        logger.warning(data)
        if interface.send_post(data=data):
            logger.warning('Успех')
        else:
            logger.warning('Провал')
        media_group_chats.remove(int(message.chat.id))
        media_group_chats.clear()



client.run()

