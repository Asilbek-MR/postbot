from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# API ID va API Hash qiymatlarini my.telegram.org orqali olishingiz mumkin
bot_token = '5754593374:AAELAHEjXIHEyS4RIBHbm8V-46h5DhNB11A'
bot_username = '@napolyon01_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Assalomu alaykum!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Assalomu alaykum! Qanday yordam berishim mumkun.')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Assalomu alaykum! Bu foydalanuvchilar uchun.')


def handle_response(text: str):
    prepare = text.lower()
    if 'hello' in prepare:
        return 'Assalomu alaykum!'
    if 'how are you' in prepare:
        return 'yaxshi raxmat'
    if 'i love python' in prepare:
        return 'python is so cool'
    return 'seni tushunmayapman nima demoqchisan...'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id} ) in {message_type}: {text}')
    
    if message_type == "group":
        if bot_username in text:
            new_text = text.replace(bot_username, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
    print(response, "bot")
    await update.message.reply_text(response)
    
async def error(update: Update,context: ContextTypes.DEFAULT_TYPE):
    print("Starting ...")
    print(f"Update {update} cause error {context.error}")
    
    if __name__ == '__main__':
        app = Application.builder().token(bot_token).build()
        app.add_handler(CommandHandler('start', start_command))
        # commandani ushlab beradi 
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CommandHandler('custom', custom_command))
        app.add_handler(MessageHandler(filters.Text, handle_message))
        app.add_error_handler(error)
        print("Polling")
        app.run_polling(poll_interval=4)









