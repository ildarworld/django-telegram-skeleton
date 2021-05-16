import pytest
from faker import Faker

fake = Faker()


class TelegramUserMock:
    def __init__(self, id, first_name, last_name, username):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


@pytest.fixture
def telegram_user():
    return TelegramUserMock(
        id=fake.numerify("##########"),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        username=fake.user_name(),
    )
