from django.test import TestCase
from django.urls import reverse, resolve
from home import views


class TestUrls(TestCase):
    def test_home_url(self):
        url = reverse('home:home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)