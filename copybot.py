
from telebot import TelegramClient, events



BOT_TOKEN = '7129894107:AAFvR_xicYQ0S7viH4K0usQemKDGmQYLZa0'
bot_username = '@appealuserbot'
# CHANNEL_USERNAME = enginer_developer
ADMIN_CHANNEL_ID = -1001518206463
API_HASH = '9ae7a9067e358b1cbae12ac0a20ff95e'
API_ID = 26230342



# Telegram Clientni sozlash
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
print('bot ishga tushdi')
# Kuzatiladigan kanal va o'z kanalingiz
source_channel = 'suvtekinn'  # Kuzatmoqchi bo'lgan kanal
target_channel = 'every_dev'  # O'zingizning kanal

# Hodisalarni kuzatish
@client.on(events.NewMessage(chats=source_channel))
async def forward_to_target(event):
    # Yangi xabarni o'z kanalingizga yuboring
    print('Forward')
    if event.message.text:
        await client.send_message(target_channel, event.message.text)
    elif event.message.photo:
        await client.send_file(target_channel, event.message.photo)
    elif event.message.video:
        await client.send_file(target_channel, event.message.video)
    else:
        await client.send_message(target_channel, event.message)

print("Bot ishga tushdi...")
client.run_until_disconnected()
