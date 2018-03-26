# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import User, Consumption

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import LineChart
from django_pandas.io import read_frame
# Create your views here.


class SummaryView(generic.TemplateView):
    template_name = 'consumption/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Summary"

        # for line Chart
        queryset = Consumption.queryset_consumption_sum_per_day()
        list_values = self.create_list_for_chart(queryset)
        data_source = SimpleDataSource(data=list_values)
        chart = LineChart(data_source)
        context['chart'] = chart
        context['chart_title'] = "Sum Consumption Line Chart"

        # for table
        queryset = User.objects.all().order_by('id')
        table = queryset
        context['table'] = table
        context['table_title'] = "User List"

        return context

    @staticmethod
    def create_list_for_chart(queryset):
        df = read_frame(queryset)
        # First element is x axis
        df = df.ix[:, ['day', 'consumption__sum', ]]
        # create value list with headers
        list_headers = df.columns.tolist()
        list_values = df.values.tolist()
        list_values.insert(0, list_headers)
        return list_values


class DetailView(generic.TemplateView):
    template_name = 'consumption/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["title"] = "Detail"
        table = Consumption.queryset_consumption_avg_per_user()
        context['table'] = table
        context['table_title'] = "Average Consumption Per User"
        return context

