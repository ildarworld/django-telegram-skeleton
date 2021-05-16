import logging
import os
import sys
import traceback

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from telegram import ParseMode
from telegram import User as TelegramUser
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler
from telegram.utils.helpers import mention_html

from bot.models import Profile
from bot.decorators import restricted
from bot.handlers import TelegramChannelHandler

import logging

log = logging.getLogger("bot")


class Bot:
    def __init__(self, token=None):
        """Only if token has been provided telegram bot will starts
        Otherwise rest methdods will be testable
        """
        if token:
            self.updater = Updater(token, use_context=True)

    def start_bot(self):
        self._register_handlers()
        log.info("Bot has started")
        self._start_polling()

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    def _register_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("users_number", self.users_number))
        self.dispatcher.add_error_handler(self.error)

    def _start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update=None, context=None):
        """Send message on `/start`."""
        tg_user = update.message.from_user
        profile = None
        try:
            profile = Profile.objects.get(tg_user_id=tg_user.id)
        except ObjectDoesNotExist:
            log.info("New user has joined")
            profile = self._create_user(tg_user)
            #  Here some come to proccess start behaviour for new user
        else:
            self._update_user(profile, tg_user)
            log.info("Existing user has sent message")
            #  Here some come to proccess start behaviour for exist user
        update.message.reply_text(_(f"Hello {tg_user.username}"))

    """ Creating django user as well as Telegram Profile
    """

    def _create_user(self, tg_user: TelegramUser) -> None:
        user = get_user_model().objects.create_user(
            username=tg_user.id,
            password=User.objects.make_random_password(),
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
        )
        user.refresh_from_db()
        profile = Profile.objects.create(
            user=user,
            tg_user_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            tg_username=tg_user.username,
            active=True,
            created_by="TELEGRAM_BOT",
        )
        return profile

    """Updating user in case the user has changed name or username
    """

    def _update_user(self, profile: Profile, tg_user: TelegramUser) -> None:
        profile.first_name = tg_user.first_name
        profile.last_name = tg_user.last_name
        profile.username = tg_user.username
        profile.save()

    @restricted
    def users_number(self, update, context):
        update.message.reply_text(
            text=_(
                "Number of active users: *{}*".format(
                    Profile.objects.filter(active=True).count()
                )
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    def error(self, update, context):
        log.error(_("Error happened in bot"))
        trace = "".join(traceback.format_tb(sys.exc_info()[2]))
        payload = ""
        if not update:
            return
        if update.effective_user:
            payload += f" with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}"
        if update.effective_chat:
            payload += f" within the chat <i>{update.effective_chat.title}</i>"
            if update.effective_chat.username:
                payload += f" (@{update.effective_chat.username})"
        if update.poll:
            payload += f" with the poll id {update.poll.id}."
        text = _(
            f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}"
            f"</code>"
        )

        for dev_id in settings.LIST_OF_ADMINS:
            context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
