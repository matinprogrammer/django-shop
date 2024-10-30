from django.test import TestCase
from django.urls import reverse
from category import models


class TestHomeView(TestCase):
    def test_home_view_GET(self):
        response = self.client.get(reverse('home:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')