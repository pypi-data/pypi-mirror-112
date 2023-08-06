import os

import telegram
from flask import Flask, request

from .telegram_bot import handler, start_command, help_command, contact_command

global bot, bot_token, webhook_host, webhook_url
bot_token = os.environ.get('BOT_TOKEN', 'dummy_token')
webhook_host = os.environ.get('WEBHOOK_HOST', '157.245.38.24')
webhook_port = os.environ.get('WEBHOOK_PORT', 8443)
webhook_url = os.environ.get('WEBHOOK_URL', 'dummy_url')
bot = telegram.Bot(token=bot_token)
cert = 'cert.pem'
cert_key = 'key.pem'
context = (cert, cert_key)
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
    s = bot.setWebhook(webhook_url, certificate=open(cert, 'rb'))
    if s:
        return f"Webhook setup OK : {webhook_url}"
    else:
        return f"Webhook setup failed : {webhook_url}"


@app.route('/')
def index():
    return '<h1>Tabayyun Bot webhook is running</h1>'


def start():
    app.run(threaded=True, port=webhook_port, host=webhook_host, ssl_context=context)


if __name__ == '__main__':
    start()
