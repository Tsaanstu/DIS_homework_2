from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/')


class Client(models.Model):
    full_name = models.CharField(max_length=30)
    login = models.CharField(max_length=20)
    birthday = models.DateField()
    contract_number = models.CharField(max_length=10)
    date_conclusion = models.DateField()
    tel = models.CharField(max_length=12)
    address = models.CharField(max_length=100)


class Account(models.Model):
    update_time = models.DateField()
    currency = models.CharField(max_length=3)
    balance = models.FloatField()
    cl_id = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
    )


class History_of_changes(models.Model):
    old_balance = models.FloatField()
    new_balance = models.FloatField()
    reason = models.CharField(max_length=30)
    update_time = models.DateField()
    acc_id = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
    )


class Transfer(models.Model):
    tr_date = models.DateField()
    source_currency = models.CharField(max_length=3)
    source_sum = models.FloatField()
    final_currency = models.CharField(max_length=3)
    final_sum = models.FloatField()
    source_his_id = models.ForeignKey(
        'History_of_changes',
        related_name='source_his_id',
        on_delete=models.CASCADE,
    )
    final_his_id = models.ForeignKey(
        'History_of_changes',
        related_name='final_his_id',
        on_delete=models.CASCADE,
    )


class Rate(models.Model):
    source_currency = models.CharField(max_length=3)
    final_currency = models.CharField(max_length=3)
    cost = models.FloatField()
    update = models.DateField()
