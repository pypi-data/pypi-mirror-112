#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from sqlite3 import connect

import pandas as pd
from telegram import Update, ForceReply
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from src.dataclasses.chat import Chat
from src.service.server import Server

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
server = Server()


# Define a few command handlers. These usually take the two arguments update and
# context.
def start_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hallo {user.mention_markdown_v2()}\! Silahkan masukan artikel/topik yang hendak dianalisa',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """📜 Petunjuk penggunaan :
        
Silahkan masukan/forward artikel atau postingan di sini, maka bot akan memulai menganalisa apakah postingan/artikel tersebut mengandung informasi yang valid atau tidak (Hoax). 
Kamu juga bisa masukan topik apapun untuk dianalisa apakah saat ini ada berita atau hoax terkait topik tersebut
        """)


def contact_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Pertanyaan atau saran bisa hubungi @azzambz")


def handler(update: Update, context: CallbackContext = None) -> None:
    """Echo the user message."""
    chat = Chat(
        chat_id=update.message.chat_id,
        sender_id=update.message.from_user.username,
        sender=update.message.from_user.first_name,
        str_message=update.message.text
    )
    svr = Server()
    try:
        update.message.reply_text(svr.handler(chat))
    except BadRequest as br:
        update.message.reply_text("Kata/Kalimat terlalu umum, silahkan masukan artikel/topik yang hendak dianalisa!")


def pickling_dataset():
    dataset_db = os.environ.get('HOAX_DATABASE')
    conn = connect(dataset_db)
    df = pd.read_sql("select link, tittle, content, status from articles", conn)
    df.to_pickle("tabayyun.pkl")


def start_bot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    if os.environ.get('BOT_TOKEN'):
        token = os.environ['BOT_TOKEN']
    else:
        token = "1864795084:AAGbZZmCF3oK7q5opPZUatLw3KzguMH7fYU"

    updater = Updater(token)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # pickling dataset
    pickling_dataset()

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("contact", contact_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    start_bot()
