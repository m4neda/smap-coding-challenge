# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.PositiveIntegerField()
    area = models.CharField(max_length=128)
    tariff = models.CharField(max_length=128)

    def __str__(self):
        return '{0}'.format(self.user_id)


class Consumption(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    consumption = models.PositiveIntegerField()

    def __str__(self):
        return '{0}'.format(self.user_id)

