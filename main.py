import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from telethon import functions, types
from telethon.tl.functions.messages import SendMessageRequest

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
# admin_channel_id = get_env_value('ADMIN_CHANNEL_ID')
admin_channel_id = -1001518206463

# Clientni yaratish
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
builder = client.build_reply_markup

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Userdan kontaktini yuborishini so'rash
    await event.respond('Iltimos, kontaktingizni ulashing:', buttons=[
        types.KeyboardButtonRequestPhone('Kontaktingizni ulashing')
    ])

# @client.on(events.NewMessage)
# async def add_contact_and_invite(event):
#     if event.contact:
#         print(event)
#         contact = event.contact
#         try:
#             user = await client.get_entity(contact.user_id)
            
#             # Foydalanuvchini kanalingizga qo'shish
#             try:
#                 await client(InviteToChannelRequest(channel=channel_username, users=[user.id]))
#                 await event.respond('Sizning kontakt raqamingiz qabul qilindi va siz kanalga qo\'shildingiz.')
#             except UserPrivacyRestrictedError:
#                 await event.respond('Kechirasiz, foydalanuvchini kanalga qo\'shib bo\'lmaydi, chunki uning shaxsiy sozlamalari bunga ruxsat bermaydi.')
#             except UserAlreadyParticipantError:
#                 await event.respond('Foydalanuvchi allaqachon kanalga qo\'shilgan.')
#         except Exception as e:
#             await event.respond(f'Kontakt qo\'shishda xatolik yuz berdi: {str(e)}')
#     else:
#         await event.respond('Iltimos, kontakt raqamingizni yuboring.')


@client.on(events.NewMessage(func=lambda e: e.contact))
async def contact_handler(event):
    contact = event.contact
    user = await event.get_sender()

    user_info = (
        f"User ID: {user.id}\n"
        f"Username: {user.username}\n"
        f"Name: {user.first_name} {user.last_name}\n"
        f"Phone: {contact.phone_number}\n"
        # f"Message: {event.message.message}"
    )

    # Send message to the admin channel
    await client.send_message(admin_channel_id, user_info)

    # Respond to the user
    await event.respond('Your contact has been received and forwarded to the admin channel.')
    




# Clientni ishga tushiring
client.run_until_disconnected()
