"""" Command line interface for the bot"""
import logging

import click
import colorama
from pyfiglet import figlet_format
from termcolor import colored
from src.view import telegram_bot
from src.service import crawler

colorama.init()
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

@click.command()
@click.option('--start', is_flag=True, help='Start the bot')
@click.option('--crawl', is_flag=True, help='Start the bot')
def handle_commands(start, crawl):
    """Main method for handling commands through CLI"""
    stdout("Tabayyun Bot", color="blue", figlet_flag=True)
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
            crawler.start()
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
