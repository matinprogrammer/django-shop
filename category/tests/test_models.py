from audioop import reverse

from django.test import TestCase
from category.models import Category, Product
from model_bakery import baker


class TestCategoryModel(TestCase):
    def test_model_str(self):
        category = baker.make(Category, slug='test-category')
        self.assertEqual(str(category), 'test-category')

class TestProductModel(TestCase):
    def test_model_str(self):
        product = baker.make(Product, slug='test-product')
        self.assertEqual(str(product), 'test-product')

