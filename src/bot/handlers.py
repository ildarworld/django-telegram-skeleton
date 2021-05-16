from logging import Handler, LogRecord


""" Custom logging hablder which will take global bot in other to have
    possibility to send logs to channel
"""


class TelegramChannelHandler(Handler):
    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id

    def emit(self, record: LogRecord):
        try:
            """Import is here because during loading this Handler app (bot) is not started yet"""
            from bot.management.commands.start_bot import bot

            msg = self.format(record)

            if bot:
                result = bot.updater.bot.send_message(
                    self.channel_id,
                    text=msg,
                )

        except Exception as ex:
            print("Exception ", ex)
