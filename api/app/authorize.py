import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")


def main():
    with Client("djangoclient", api_id, api_hash) as client:
        print("Сессия создана.")


if __name__ == "__main__":
    main()
