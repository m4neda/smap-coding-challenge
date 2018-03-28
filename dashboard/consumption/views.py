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

        chart = self.create_line_chart_consumption_sum()
        context['chart'] = chart
        context['chart_title'] = "Sum Consumption Line Chart"

        context['table'] = Consumption.queryset_consumption_avg_per_user()
        context['table_title'] = "Average Consumption Per User"

        return context

    def create_line_chart_consumption_sum(self):
        queryset = Consumption.queryset_consumption_sum_per_day()
        df = self.create_dataframe_for_chart_consumption_sum(queryset)
        list_values = self.dataframe_to_list_with_header(df)
        data_source = SimpleDataSource(data=list_values)
        chart = LineChart(data_source)
        return chart

    @staticmethod
    def create_dataframe_for_chart_consumption_sum(queryset):
        df = read_frame(queryset)
        # First element is x axis, in django_graphos
        df = df.ix[:, ['day', 'consumption__sum', ]]
        return df

    @staticmethod
    def dataframe_to_list_with_header(df):
        list_headers = df.columns.tolist()
        list_values = df.values.tolist()
        list_values.insert(0, list_headers)
        return list_values


class DetailView(generic.TemplateView):
    template_name = 'consumption/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["title"] = "Detail"
        return context

