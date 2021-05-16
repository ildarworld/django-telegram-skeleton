# Generated by Django 3.2.3 on 2021-05-15 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('tg_user_id', models.IntegerField(unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('tg_username', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('active', models.BooleanField(default=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('email', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('provider_payment_charge_id', models.CharField(max_length=100, null=True)),
                ('paid_message_id', models.IntegerField()),
                ('paid_for', models.CharField(max_length=200, null=True)),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
