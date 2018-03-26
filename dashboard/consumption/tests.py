# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings

from .models import User, Consumption, Round

from datetime import datetime
from pytz import timezone

from django.urls import reverse
# Create your tests here.


class UrlResolveTests(TestCase):
    def test_url_resolves_to_index_view(self):
        response = self.client.get(reverse('consumption:index'))
        self.assertEqual(200, response.status_code)

    def test_url_resolves_to_summary_view(self):
        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(200, response.status_code)

    def test_url_resolves_to_detail_view(self):
        response = self.client.get(reverse('consumption:detail'))
        self.assertEqual(200, response.status_code)


class SummaryViewTests(TestCase):
    def test_table_html(self):
        response = self.client.get(reverse('consumption:summary'))

        self.assertContains(response, "<th>user</th>")
        self.assertContains(response, "<th>area</th>")
        self.assertContains(response, "<th>tariff</th>")

    def test_empty_table(self):
        response = self.client.get(reverse('consumption:summary'))

        self.assertQuerysetEqual(response.context['table'], [])
        self.assertNotContains(response, "<td>")

    def test_not_empty_table(self):
        user = User.objects.create(id=3000, area="a1", tariff="t1")

        response = self.client.get(reverse('consumption:summary'))

        self.assertQuerysetEqual(response.context['table'], ['<User: 3000>'])
        self.assertContains(response, user.id)
        self.assertContains(response, user.area)
        self.assertContains(response, user.tariff)


class DetailViewTests(TestCase):
    def test_table_html(self):
        response = self.client.get(reverse('consumption:detail'))

        self.assertContains(response, "<th>user</th>")
        self.assertContains(response, "<th>consumption_avg</th>")

        self.assertQuerysetEqual(response.context['table'], [])


class UserTests(TestCase):
    def test_no_users(self):
        user_list = User.objects.all()
        self.assertEqual(user_list.count(), 0)

    def test_saving_and_retrieving_user(self):
        user_id, area, tariff = 1, 'a1', 't1'
        save_user(user_id, area, tariff)
        saved_user = User.objects.all()
        actual_user = saved_user[0]

        self.assertEqual(saved_user.count(), 1)
        self.assertEqual(actual_user.id, user_id)
        self.assertEqual(actual_user.area, area)
        self.assertEqual(actual_user.tariff, tariff)


def save_user(user_id, area, tariff):
    first_user = User()
    first_user.id = user_id
    first_user.area = area
    first_user.tariff = tariff
    first_user.save()


def save_consumption(user, datetime_val, consumption):
    consumption_data = Consumption()
    consumption_data.user = user
    consumption_data.datetime = datetime_val
    consumption_data.consumption = consumption
    consumption_data.save()


class ConsumptionTests(TestCase):
    def test_saving_and_retrieving_consumption(self):
        user_id, area, tariff = 1, 'a1', 't1'
        save_user(user_id, area, tariff)

        user = User.objects.get(id=user_id)
        datetime_str = '2016-07-15 00:00:00'
        datetime_val = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').astimezone(timezone(settings.TIME_ZONE))
        consumption = 100
        save_consumption(user, datetime_val, consumption)

        saved_consumption = Consumption.objects.all()
        actual_data = saved_consumption[0]

        self.assertEqual(saved_consumption.count(), 1)
        self.assertEqual(actual_data.user, user)
        self.assertEqual(actual_data.datetime, datetime_val)
        self.assertEqual(actual_data.consumption, consumption)

