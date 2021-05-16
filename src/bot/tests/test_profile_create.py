import pytest

from django.conf import settings
from django.contrib.auth import get_user_model

from bot.bot import Bot
from bot.models import Profile


@pytest.mark.django_db
def test_create_user_profile(telegram_user):
    bot = Bot()
    bot._create_user(telegram_user)
    profile = Profile.objects.last()
    assert profile.tg_username == telegram_user.username
    assert get_user_model().objects.last().username == telegram_user.id
