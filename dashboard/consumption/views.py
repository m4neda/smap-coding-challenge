# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import User, Consumption
from .tables import UserTable

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import LineChart
from django_pandas.io import read_frame
from django_tables2 import RequestConfig
# Create your views here.


class SummaryView(generic.TemplateView):
    template_name = 'consumption/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Summary"

        # for line Chart
        queryset = Consumption.queryset_consumption_avg_per_day()
        list_values = self.create_list_for_chart(queryset)
        data_source = SimpleDataSource(data=list_values)
        chart = LineChart(data_source)
        context['chart'] = chart

        # for table
        queryset = User.objects.all()
        table = UserTable(queryset)
        RequestConfig(self.request).configure(table)
        context['table'] = table

        return context

    @staticmethod
    def create_list_for_chart(queryset):
        df = read_frame(queryset)
        # round
        df['consumption__avg'] = df['consumption__avg'].round()
        # First element is x axis
        df = df.ix[:, ['day', 'consumption__avg', ]]
        # create value list with headers
        list_headers = df.columns.tolist()
        list_values = df.values.tolist()
        list_values.insert(0, list_headers)
        return list_values


class DetailView(generic.TemplateView):
    template_name = 'consumption/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["message"] = "Detail View"
        return context

