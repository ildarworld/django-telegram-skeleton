from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from bot.bot import Bot

""" Making bot pointer available from outside e.g. in order to send
    logs to Telegram channel

    To start bot just execute:
    >>> python manage.py start_bot
"""
bot = None


class Command(BaseCommand):
    def handle(self, *args, **options):
        global bot
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.start_bot()
