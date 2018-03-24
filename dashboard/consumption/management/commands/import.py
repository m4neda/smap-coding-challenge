from django.core.management.base import BaseCommand
from django.conf import settings

import csv
import os
from os.path import join, relpath
from glob import glob

from datetime import datetime
from ...models import User, Consumption
from pytz import timezone


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        user_data_path = '../data/user_data.csv'
        consumption_path = '../data/consumption/'

        self.read_user_data(user_data_path)
        self.read_consumption(consumption_path)

    @staticmethod
    def read_consumption(path):
        # get csv file name list
        files = [relpath(x, path) for x in glob(join(path, '*.csv'))]
        for file in files:
            # separate filename ext
            user_id, _ext = os.path.splitext(file)

            with open(path + file) as f:
                reader = csv.reader(f, delimiter=',')
                _header = next(reader)
                user = User.objects.get(id=int(user_id))

                Consumption.objects.bulk_create([Consumption(
                    user=user,
                    datetime=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').astimezone(timezone(settings.TIME_ZONE)),
                    consumption=float(row[1]),
                ) for row in reader])

    @staticmethod
    def read_user_data(path):
        with open(path) as f:
            reader = csv.reader(f, delimiter=',')
            _header = next(reader)
            User.objects.bulk_create([User(
                id=row[0],
                area=row[1],
                tariff=row[2],
            ) for row in reader])

