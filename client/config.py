import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

client = Client('pyroclient', os.getenv('API_ID'), os.getenv('API_HASH'))

