import os

import telegram
from flask import Flask, request

from .telegram_bot import handler, start_command, help_command, contact_command

global bot, bot_token, webhook_url
bot_token = os.environ.get('BOT_TOKEN', 'dummy_token')
webhook_url = os.environ.get('WEBHOOK_URL', 'dummy_url')
bot = telegram.Bot(token=bot_token)

app = Flask(__name__)


@app.route('/tabayyun-bot', methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message.text == "/start":
        start_command(update)
    elif update.message.text == "/help":
        help_command(update)
    elif update.message.text == "/contact":
        contact_command(update)
    else:
        handler(update)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=webhook_url, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '<h1>Tabayyun Bot webhook is running</h1>'


def start():
    app.run(threaded=True, port=8443)


if __name__ == '__main__':
    start()
