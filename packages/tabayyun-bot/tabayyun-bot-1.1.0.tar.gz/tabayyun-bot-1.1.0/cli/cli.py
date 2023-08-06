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

from src.service import crawler
from src.view import telegram_bot

colorama.init()
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


@click.command()
@click.option('--start', is_flag=True, help='Start the bot')
@click.option('--crawl', is_flag=True, help='Start the bot')
def handle_commands(start, crawl):
    """Main method for handling commands through CLI"""
    if not os.environ.get('HOAX_DATA_PATH') or not os.environ.get('BOT_TOKEN'):
        stdout("ERROR: please set HOAX_DATA_PATH and BOT_TOKEN to start the bot! ", color="red")
        sys.exit(1)
    stdout("\nTabayyun Bot", color="blue", figlet_flag=True)
    if start:
        stdout("Starting tabayyun server...", color="green")
        try:
            telegram_bot.start_bot()
            stdout("Server started", color="green")
        except Exception as exc:
            stdout("Starting server failed! : {}".format(exc), color="red")

    if crawl:
        stdout("Crawling news...", color="green")
        try:
            crawler.start(os.environ.get('HOAX_DATA_PATH'))
            stdout("Crawling completed!", color="green")
        except Exception as exc:
            stdout("Crawling failed! : {}".format(exc), color="red")


def stdout(string: str, color: str, font: str = "slant", figlet_flag: bool = False):
    """ A helper method to print logs to stdout """
    if not figlet_flag:
        logging.info(colored(string, color))
    else:
        logging.info(colored(figlet_format(string, font=font), color))


if __name__ == "__main__":
    handle_commands()
