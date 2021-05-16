# Small Django-Telegram bot

Welcome to django-telegram-bot skeleton which out of the box able to register telegram bots users and keep them in db.

Also, there is functionality to send logs through standard python logger to Telegram channel where
the bot is admin with permission to send messages

## Start bot

Before start bot please fill .env file (or create system environemnt variables) with data like in .env.example

E.g. copy docs/env.exmaple file:

`cp ./docs/.env.example ./src/.env`

Fill all the required fields in ./club/env, such as TELEGRAM_BOT_TOKEN etc.

TELEGRAM_BOT_TOKEN you can get from @BotFather.

To get TELEGRAM_CHANNEL_ID etc Just Simply Forward a message from your group/channel to @JsonDumpBot or @getidsbot

Run bot:

`cd src && python manage.py start_bot`
