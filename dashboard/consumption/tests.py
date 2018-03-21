# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.urls import reverse
# Create your tests here.


class UrlResolveTests(TestCase):
    def test_url_resolves_to_index_view(self):
        response = self.client.get(reverse('consumption:index'))
        self.assertEqual(200, response.status_code)

    def test_url_resolves_to_summary_view(self):
        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(200, response.status_code)

