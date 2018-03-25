from django.conf import settings
from django.conf.urls import include, url
from .views import SummaryView, DetailView

app_name = 'consumption'

urlpatterns = [
    url(r'^$', SummaryView.as_view(), name='index'),
    url(r'^summary/', SummaryView.as_view(), name='summary'),
    url(r'^detail/', DetailView.as_view(), name='detail'),
]
