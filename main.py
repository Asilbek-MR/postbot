import os
from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError
from dotenv import load_dotenv
from telethon.tl.types import InputPhoneContact, User
from telethon import functions, types

class ImproperlyConfigured(Exception):
    pass

def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg)

# .env faylini yuklash
load_dotenv()

# Muhit o'zgaruvchilarini olish
api_id = get_env_value('API_ID')
api_hash = get_env_value('API_HASH')
bot_token = get_env_value('BOT_TOKEN')
channel_username = get_env_value('CHANNEL_USERNAME')

# Clientni yaratish
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
builder = client.build_reply_markup

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Userdan kontaktini yuborishini so'rash
    await event.respond('Iltimos, kontaktingizni ulashing:', buttons=[
        types.KeyboardButtonRequestPhone('Kontaktingizni ulashing')
    ])
    

@client.on(events.NewMessage)
async def add_contact_and_invite(event):
    if event.contact:
        print(event)
        contact = event.contact
        try:
            user = await client.get_entity(contact.user_id)
            
            # Foydalanuvchini kanalingizga qo'shish
            try:
                await client(InviteToChannelRequest(channel=channel_username, users=[user.id]))
                await event.respond('Sizning kontakt raqamingiz qabul qilindi va siz kanalga qo\'shildingiz.')
            except UserPrivacyRestrictedError:
                await event.respond('Kechirasiz, foydalanuvchini kanalga qo\'shib bo\'lmaydi, chunki uning shaxsiy sozlamalari bunga ruxsat bermaydi.')
            except UserAlreadyParticipantError:
                await event.respond('Foydalanuvchi allaqachon kanalga qo\'shilgan.')
        except Exception as e:
            await event.respond(f'Kontakt qo\'shishda xatolik yuz berdi: {str(e)}')
    else:
        await event.respond('Iltimos, kontakt raqamingizni yuboring.')

# Clientni ishga tushiring
client.run_until_disconnected()
