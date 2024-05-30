import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from telethon import functions, types
from telethon.tl.functions.messages import SendMessageRequest
import time

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

    

@client.on(events.NewMessage(func=lambda e: e.contact))
async def contact_handler(event):
    contact = event.contact
    if contact:
        user = await event.get_sender()
        user_info = (
            f"📚 User ID: {user.id}\n"
            f"👨🏻‍💻 Username: {user.username}\n"
            f"🔎  Name: {user.first_name} {user.last_name}\n"
            f"🤳 Phone: {contact.phone_number}\n"     
        )
        # Send message to the admin channel
        await client.send_message(admin_channel_id, user_info)
    else:
        pass

user_data = {}

questions = [
    "🚗Moshina modeli:",
    "🔢Pozitsiya:",
    "🛠Kraska:",
    "♻️Rangi:",
    "📊Yil:",
    "🛞Probeg:",
    "⛽️Benzin:",
    "💰Narxi:",
    "📞Tel:",
    "📍Shaxar:",
    "Iltimos, moshinaning rasmini yuboring:"
]

keys = [
    "modeli",
    "pozitsiya",
    "kraska",
    "rangi",
    "yili",
    "probeg",
    "benzin",
    "narxi",
    "tel",
    "shaxar"
]
@client.on(events.NewMessage)
async def handle_message(event):
    chat_id = event.chat_id

    if chat_id not in user_data:
        user_data[chat_id] = {'index': 0, 'data': {}}
        await client.send_message(chat_id, questions[0])
        user_data[chat_id]['index'] += 1
    else:
        index = user_data[chat_id]['index']
        if index <= len(keys):
            user_data[chat_id]['data'][keys[index - 1]] = event.message.message
            if index < len(questions) - 1:
                await client.send_message(chat_id, questions[index])
                user_data[chat_id]['index'] += 1
            elif index == len(questions) - 1:
                await client.send_message(chat_id, questions[index])
                user_data[chat_id]['index'] += 1
        elif index == len(questions):
            if event.message.photo:
                photo = event.message.photo
                path = await client.download_media(photo, file=f"./{chat_id}_car_photo.jpg")
                user_data[chat_id]['data']['photo'] = path
                collectdata = user_data[chat_id]['data']
                info = (
                    f"🚗Moshina modeli: {collectdata.get('modeli')}\n"
                    f"🔢Pozitsiya: {collectdata.get('pozitsiya')}\n"
                    f"🛠Kraska: {collectdata.get('kraska')}\n"
                    f"♻️Rangi: {collectdata.get('rangi')}\n"
                    f"📊Yil: {collectdata.get('yili')}\n"
                    f"🛞Probeg: {collectdata.get('probeg')}\n"
                    f"⛽️Benzin: {collectdata.get('benzin')}\n"
                    f"💰Narxi: {collectdata.get('narxi')}\n"
                    f"📞Tel: {collectdata.get('tel')}\n"
                    f"📍Shaxar: {collectdata.get('shaxar')}\n"
                )
                await client.send_file(chat_id, path, caption=info)
                await client.send_file(admin_channel_id,path, caption=info)
                user_data.pop(chat_id)
            else:
                await client.send_message(chat_id, "Iltimos, moshinaning rasmini yuboring:")
                
# Clientni ishga tushiring
client.run_until_disconnected()
