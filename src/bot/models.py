from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tg_user_id = models.IntegerField(unique=True)

    """ Duplicating first name and last name here made consciously in
        order to have separate info for telegram user and users registered via 
        standard django auth process
    """
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    tg_username = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

    """Fields above will be updated after payment through Telegram
    """
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    email = models.CharField(max_length=50, null=True, blank=True, default=None)

    def __repr__(self):
        return _("")


class Payment(TimeStampedModel):
    partner = models.ForeignKey("bot.Profile", null=True, on_delete=models.SET_NULL)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    provider_payment_charge_id = models.CharField(max_length=100, null=True)
    paid_message_id = models.IntegerField()
    paid_for = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.partner.tg_user_id} paid {self.total_amount} provider info ({self.provider_payment_charge_id}) for {self.paid_for}"
