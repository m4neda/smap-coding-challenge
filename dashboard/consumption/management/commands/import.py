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

    def read_consumption(self):
        path = self.consumption_path

        # get csv file name list
        files = [relpath(x, path) for x in glob(join(path, '*.csv'))]
        for file in files:
            # separate filename ext
            user_id, _ext = os.path.splitext(file)

            with open(path + file) as f:
                reader = csv.reader(f)
                _header = next(reader)

                for row in reader:
                    consumption = float(row[1])
                    datetime_val = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').astimezone(timezone(settings.TIME_ZONE))
                    _, created = Consumption.objects.get_or_create(
                        user_id= User.objects.get(user_id=int(user_id)),
                        datetime=datetime_val,
                        consumption=consumption,
                    )


    def read_user_data(self):
        path = self.user_data_path

        with open(path) as f:
            reader = csv.reader(f)
            _header = next(reader)
            for row in reader:
                _, created = User.objects.get_or_create(
                    user_id=row[0],
                    area=row[1],
                    tariff=row[2],
                )


    def handle(self, *args, **options):
        self.user_data_path = '../data/user_data.csv'
        self.consumption_path = '../data/consumption/'

        self.read_user_data()
        self.read_consumption()
