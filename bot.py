import json
import logging

import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from config import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Добрый день!\n" "Чтобы сгенерировать заголовок, просто отправь мне текст",
    )


def __get_headline(text):
    headline = requests.post(
        "http://0.0.0.0:5000/translator/translate",
        data=json.dumps([{"id": 1, "src": text}]),
        headers={"Content-type": "application/json"},
    ).json()

    return headline


def get_headline(update: Update, context: CallbackContext):
    text = update.message.text

    keywords = __get_headline(text)

    context.bot.send_message(chat_id=update.message.chat_id, text=f"{keywords}")


start_handler = CommandHandler("start", start)
conv_handler = MessageHandler(filters=Filters.text, callback=get_headline, pass_user_data=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)


updater.start_polling()
