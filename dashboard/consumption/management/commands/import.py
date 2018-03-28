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

    def __init__(self):
        self.user_data_path = os.path.join(settings.DATA_DIR, settings.IMPORT_USER_DATA_PATH)
        self.consumption_path = os.path.join(settings.DATA_DIR, settings.IMPORT_CONSUMPTION_PATH)

    def handle(self, *args, **options):
        user_data_path = self.user_data_path
        consumption_path = self.consumption_path

        self.read_user_data(user_data_path)
        self.read_consumption(consumption_path)

    @staticmethod
    def read_consumption(path):
        # get all csv file name list
        files = [relpath(x, path) for x in glob(join(path, '*.csv'))]
        for file in files:
            # separate filename ext
            user_id, _ext = os.path.splitext(file)
            filepath = os.path.join(path, file)
            with open(filepath) as f:
                reader = csv.reader(f, delimiter=',')
                _header = next(reader)
                user = User.objects.get(id=int(user_id))

                Consumption.objects.bulk_create([Consumption(
                    user=user,
                    datetime=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').astimezone(timezone(settings.TIME_ZONE)),
                    consumption=int(float(row[1])),
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

