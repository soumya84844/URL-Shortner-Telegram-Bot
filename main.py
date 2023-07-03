from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN : Final = '6363426494:AAFzGHk3cdUGJeg_RpT6TK9dOt19jhI7jKQ'
BOT_USERNAME : Final = '@Soumya_URL_Shortner_Bot'

async def start_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Welcome to Soumya\'s URL Shortener Bot!!!')

async def help_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type a valid URL so that I can Shorten it!!!')

def handle_response(url : str) -> str:
    api = 'https://cleanuri.com/api/v1/shorten'
    param = {'url' : url}

    response = requests.post(api, data = param)
    json = eval(response.text)

    try:
        short_url = json['result_url'].replace('\\', '')
        return short_url
    except:
        return 'Please enter a valid URL'
    
async def handle_message(update : Update, context : ContextTypes.DEFAULT_TYPE):
    message_type : str = update.message.chat.type
    text : str = update.message.text

    if(message_type == 'group'):
        if BOT_USERNAME in text:
            new_text : str = text.replace(BOT_USERNAME, '').strip()
            response : str = handle_response(new_text)
        else:
            return
    else:
        response : str = handle_response(text)

    await update.message.reply_text(response)

async def error(update : Update, context : ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot.......')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling.......')
    app.run_polling(poll_interval=1)