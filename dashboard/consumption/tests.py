# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import User, Consumption

from django.urls import reverse
# Create your tests here.


class UrlResolveTests(TestCase):
    def test_url_resolves_to_index_view(self):
        response = self.client.get(reverse('consumption:index'))
        self.assertEqual(200, response.status_code)

    def test_url_resolves_to_summary_view(self):
        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(200, response.status_code)


class UserTests(TestCase):
    def test_no_users(self):
        user_list = User.objects.all()
        self.assertEqual(user_list.count(), 0)

    def test_saving_and_retrieving_user(self):
        first_user = User()
        id, area, tariff = 1, 'a1', 't1'
        first_user.id = id
        first_user.area = area
        first_user.tariff = tariff
        first_user.save()

        saved_user = User.objects.all()
        actual_user = saved_user[0]

        self.assertEqual(actual_user.id, id)
        self.assertEqual(actual_user.area, area)
        self.assertEqual(actual_user.tariff, tariff)

