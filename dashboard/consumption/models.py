# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    area = models.CharField(max_length=128)
    tariff = models.CharField(max_length=128)

    def __str__(self):
        return '{0}'.format(self.id)


class Consumption(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    consumption = models.PositiveIntegerField()

    def __str__(self):
        return '{0}'.format(self.user)

    @staticmethod
    def get_avg_consumption_groupby_user():
        return Consumption.objects.values('user__id').annotate(models.Avg('consumption'))

    @staticmethod
    def queryset_consumption_avg_per_day():
        queryset = Consumption.objects.all() \
            .extra(select={'day': 'date( datetime )'}) \
            .values('day') \
            .annotate(models.Avg('consumption'))
        return queryset


