"""" Command line interface for the bot"""
import logging
import os
import sys

import click
import colorama
from pyfiglet import figlet_format
from termcolor import colored

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)

colorama.init()
logging.basicConfig(level=logging.INFO, format='%(message)s')


@click.command()
@click.option('--poll', is_flag=True, help='Start the bot')
@click.option('--crawl', is_flag=True, help='Start the bot')
@click.option('--start', is_flag=True, help='Start the bot')
def handle_commands(poll, crawl, start):
    """Main method for handling commands through CLI"""
    if not os.environ.get('HOAX_DATABASE') or not os.environ.get('BOT_TOKEN'):
        stdout("ERROR: please set HOAX_DATABASE and BOT_TOKEN to start the bot! ", color="red")
        sys.exit(1)
    database = os.environ.get('HOAX_DATABASE')
    stdout("\nTabayyun Bot", color="blue", figlet_flag=True)
    if poll:
        stdout("Starting polling messages...", color="green")
        try:
            from src.view import telegram_bot
            telegram_bot.start_bot()
            stdout("Server completed", color="green")
        except Exception as exc:
            stdout("Starting server failed! : {}".format(exc), color="red")

    if crawl:
        stdout("Masukan jumlah halaman yang mau di download :", color="yellow")
        crawling_page = int(input())
        try:
            from src.service import crawler
            from src.dataset import model
            stdout("Applying schema...", color="yellow")
            stdout(f"Using database {database}", color="yellow")
            model.apply_schema(database)
            stdout("Start crawling...", color="yellow")
            crawler.start(database, crawling_page)
            stdout("Crawling completed!", color="green")
        except Exception as exc:
            stdout("Crawling failed! : {}".format(exc), color="red")

    if start:
        if not os.environ.get('WEBHOOK_URL'):
            stdout("ERROR: WEBHOOK_URL needs to be set for starting webhook server! ", color="red")
        if not os.environ.get('WEBHOOK_HOST'):
            stdout("WARNING: WEBHOOK_HOST is not set, set default value : 157.245.38.24", color="yellow")
        if not os.environ.get('WEBHOOK_PORT'):
            stdout("WARNING: WEBHOOK_PORT is not set, set default value : 8443", color="yellow")
        else:
            stdout(f"WEBHOOK_URL : {os.environ['WEBHOOK_URL']}", color="yellow")
        stdout("Starting Tabayyun webhook server...", color="green")
        try:
            from src.view import telegram_webhook
            # telegram_webhook.set_webhook()
            telegram_webhook.start()
        except Exception as exc:
            stdout("Starting server failed! : {}".format(exc), color="red")


def stdout(string: str, color: str, font: str = "slant", figlet_flag: bool = False):
    """ A helper method to print logs to stdout """
    if not figlet_flag:
        logging.info(colored(string, color))
    else:
        logging.info(colored(figlet_format(string, font=font), color))


if __name__ == "__main__":
    handle_commands()
