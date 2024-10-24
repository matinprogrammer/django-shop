from itertools import product

from django.test import TestCase
from django.urls import reverse, resolve
from category import views, models


class TestUrls(TestCase):
    def test_product_detail_urls(self):
        url = reverse('category:product_detail',args=['test'])
        self.assertEqual(resolve(url).func.view_class, views.ProductDetailView )