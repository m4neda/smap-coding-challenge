import django_tables2 as tables
from .models import User, Consumption


class ConsumptionTable(tables.Table):

    class Meta:
        model = Consumption
        template_name = 'django_tables2/bootstrap.html'
