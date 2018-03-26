# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Func

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
    def queryset_consumption_avg_per_user():
        return Consumption.objects.values('user__id').annotate(consumption__avg=Round(models.Avg('consumption')))

    @staticmethod
    def queryset_consumption_sum_per_day():
        queryset = Consumption.objects.all() \
            .extra(select={'day': 'date( datetime )'}) \
            .values('day') \
            .annotate(models.Sum('consumption'))
        return queryset


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'
