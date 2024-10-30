from django.test import TestCase
from django.urls import reverse
from category import models
from model_bakery import baker
from orders import forms


class TestProductDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = baker.make(models.Category)
        product = baker.make(models.Product, category=category, slug='product-slug', _fill_optional=['picture'])

    def test_test_product_detail_GET(self):
        response = self.client.get(reverse('category:product_detail', args=['product-slug']))

        self.assertTemplateUsed(response, 'category/product_detail.html')
        self.failUnless(response.context['form'], forms.CartAddForm)
        self.assertEqual(response.status_code, 200)