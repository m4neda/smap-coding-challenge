# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

# Create your views here.


class SummaryView(generic.TemplateView):
    template_name = 'consumption/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Hello World!!"
        return context


class DetailView(generic.TemplateView):
    template_name = 'consumption/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["message"] = "Detail View"
        return context

