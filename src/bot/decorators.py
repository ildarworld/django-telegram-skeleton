from functools import wraps
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import logging

log = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(self, update=None, context=None, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.LIST_OF_ADMINS:
            log.warning("Unauthorized access denied for {}.".format(user_id))
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=_(f"Hi {user_first_name}!\n You are not authorized to be here!"),
            )
            return
        return func(self, update, context, *args, **kwargs)

    return wrapped
