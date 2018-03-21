from django.core.management.base import BaseCommand

import csv
import os
from os.path import join, relpath
from glob import glob

from ...models import User


class Command(BaseCommand):
    help = 'import data'

    def read_consumption(self):
        path = self.consumption_path

        # get csv file name list
        files = [relpath(x, path) for x in glob(join(path, '*.csv'))]
        for file in files:
            # separate filename ext
            user_id, _ext = os.path.splitext(file)


    def read_user_data(self):
        path = self.user_data_path

        with open(path) as f:
            reader = csv.reader(f)
            header = next(reader)
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
