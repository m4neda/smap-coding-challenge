from django.core.management.base import BaseCommand
import csv
from ...models import User


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        path = '../data/user_data.csv'
        with open(path) as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                _, created = User.objects.get_or_create(
                    user_id=row[0],
                    area=row[1],
                    tariff=row[2],
                )