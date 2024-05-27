from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import UserIsBotError
from dotenv import load_dotenv

import os
import sys

class ImproperlyConfigured(Exception):
    pass

def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg)

load_dotenv()

api_id = get_env_value('API_ID')
api_hash = get_env_value('API_HASH')
bot_token = get_env_value('BOT_TOKEN')


# Clientni yarating
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    try:
        # Foydalanuvchiga xabar yuborish
        print('send message!!')
        await client.send_message(event.sender_id, 'Salom!')
    except UserIsBotError:
        print("Bot boshqa botga xabar yubora olmaydi.")

# Clientni ishga tushiring
client.run_until_disconnected()























