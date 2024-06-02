import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

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
# channel_username = get_env_value('CHANNEL_USERNAME')
# admin_channel_id = get_env_value('ADMIN_CHANNEL_ID')
admin_channel_id = -1001878919453

# Clientni yaratish
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
builder = client.build_reply_markup

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    chat_id = event.chat_id
    print('Start')
    # Userdan kontaktini yuborishini so'rash
    await event.respond("Asslomu alaykum hush kelibsiz so'ralgan ma'lumotlarni to'liq yozing agar kamchiligi bo'lsa post o'chirilishi mumkun.")
    info = (
                        f"Misol uchun post!!\n"
                        f"🚗Moshina modeli: Kobalt, Gentra...\n"
                        f"🔢Pozitsiya: 1,2...\n"
                        f"🛠Kraska: 30,40,50 \n"
                        f"♻️Rangi: oq, qora...\n"
                        f"📊Yil: 2021,2020...\n"
                        f"🛞Probeg: 0, 1000 \n"
                        f"⛽️Yoqilg'i turi: metan\n"
                        f"💰Narxi: 10000,12000...\n"
                        f"📞Tel: 994377299\n"
                        f"📍Shaxar: Frag'ona...\n"
                        f" \n"
                        f"👉Reklaman uchun bot: @appealuserbot\n"
                        f"👉Kanalga az'o bo'ling: @every_dev\n"
                    )
    await client.send_message(chat_id,info)
    

    # await event.respond('Iltimos, kontaktingizni ulashing:', buttons=[
    #     types.KeyboardButtonRequestPhone('Kontaktingizni ulashing')
    # ])

    

# @client.on(events.NewMessage(func=lambda e: e.contact))
# async def contact_handler(event):
#     contact = event.contact
#     if contact:
#         user = await event.get_sender()
#         user_info = (
#             f"📚 User ID: {user.id}\n"
#             f"👨🏻‍💻 Username: {user.username}\n"
#             f"🔎  Name: {user.first_name} {user.last_name}\n"
#             f"🤳 Phone: {contact.phone_number}\n"     
#         )
#         # Send message to the admin channel
#         await client.send_message(-1001518206463, user_info)
#     else:
#         pass

user_data = {}

questions = [
    "🚗Moshina modeli:",
    "🔢Pozitsiya:",
    "🛠Kraska:",
    "♻️Rangi:",
    "📊Yil:",
    "🛞Probeg:",
    "⛽️Yoqilg'i turi:",
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

@client.on(events.NewMessage(pattern='/donate'))
async def start(event):
    # Userdan kontaktini yuborishini so'rash
    chat_id = event.chat_id
    info = (
                        f"Asslomu alaykum paddeshka uchun raxmat 💪\n"
                        f"Karta: 8600492942461944\n"
                        
                    )
    await client.send_message(chat_id,info)
@client.on(events.NewMessage)
async def handle_message(event):
    chat_id = event.chat_id
    message = event.message.message
    
    if message == '/donate':
        await client.send_message(chat_id,"...")
    else:
        if message == '/start':
            user_data.pop(chat_id, None)
            user_data[chat_id] = {'index': 0, 'data': {}}
            await client.send_message(chat_id, "Botga xush kelibsiz! Ma'lumotlarni kiritishni boshlaymiz.\n\n" + questions[0])
            user_data[chat_id]['index'] += 1
            return

        if chat_id not in user_data:
            user_data[chat_id] = {'index': 0, 'data': {}}
            await client.send_message(chat_id, questions[0])
            user_data[chat_id]['index'] += 1
        else:
            index = user_data[chat_id]['index']
            if index <= len(keys):
                user_data[chat_id]['data'][keys[index - 1]] = message
                if index < len(questions) - 1:
                    await client.send_message(chat_id, questions[index])
                    user_data[chat_id]['index'] += 1
                elif index == len(questions) - 1:
                    await client.send_message(chat_id, questions[index])
                    user_data[chat_id]['index'] += 1
            elif index == len(questions):
                if event.message.photo:
                    if 'photo' in user_data[chat_id]['data']:
                        await client.send_message(chat_id, "Siz allaqachon rasm yubordingiz. Qayta rasm yubora olmaysiz.")
                    else:
                        photo = event.message.photo
                        path = await client.download_media(photo, file=f"./{chat_id}_car_photo.jpg")
                        user_data[chat_id]['data']['photo'] = path
                        collectdata = user_data[chat_id]['data']

                        # Validatsiya
                        if not collectdata.get('modeli'):
                            await client.send_message(chat_id, "Moshina modeli noto'g'ri kiritildi. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('pozitsiya'):
                            await client.send_message(chat_id, "Pozitsiya noto'g'ri kiritildi. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('kraska').isdigit():
                            await client.send_message(chat_id, "Kraska raqam bilan kiritilishi kerak. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('yili').isdigit():
                            await client.send_message(chat_id, "Yil raqam bilan kiritilishi kerak. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('probeg').isdigit():
                            await client.send_message(chat_id, "Probeg raqam bilan kiritilishi kerak. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('narxi').isdigit():
                            await client.send_message(chat_id, "Narx raqam bilan kiritilishi kerak. Iltimos, qayta urinib ko'ring.")
                            return
                        if not collectdata.get('tel'):
                            await client.send_message(chat_id, "Telefon raqami noto'g'ri kiritildi. Iltimos, qayta urinib ko'ring.")
                            return

                        info = (
                            f"🚗Moshina modeli: {collectdata.get('modeli')}\n"
                            f"🔢Pozitsiya: {collectdata.get('pozitsiya')}\n"
                            f"🛠Kraska: {collectdata.get('kraska')}%\n"
                            f"♻️Rangi: {collectdata.get('rangi')}\n"
                            f"📊Yil: {collectdata.get('yili')}\n"
                            f"🛞Probeg: {collectdata.get('probeg')}km\n"
                            f"⛽️Yoqilg'i turi: {collectdata.get('benzin')}\n"
                            f"💰Narxi: {collectdata.get('narxi')}$\n"
                            f"📞Tel: {collectdata.get('tel')}\n"
                            f"📍Shaxar: {collectdata.get('shaxar')}\n"
                            f"👉Reklaman uchun bot: @appealuserbot\n"
                            f"👉Kanalga az'o bo'ling: @every_dev\n"
                        )
                        
                        # Rasimni kanalda yuborish
                        await client.send_file(admin_channel_id, path, caption=info)
                        await client.send_file(chat_id, path, caption=info)
                        
                        # Rasimni serverdan o'chirish
                        if os.path.exists(path):
                            os.remove(path)
                        
                        user_data.pop(chat_id)
                else:
                    await client.send_message(chat_id, "Iltimos, moshinaning rasmini yuboring:")


    


client.start()
client.run_until_disconnected()
