from django.test import TestCase
from django.urls import reverse, resolve
from orders import views


class TestUrls(TestCase):
    def test_cart_url(self):
        url = reverse('orders:cart')
        self.assertEqual(resolve(url).func.view_class, views.CartView)

    def test_cart_add_url(self):
        url = reverse('orders:cart_add', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.CartAddView)

    def test_cart_remove_url(self):
        url = reverse('orders:cart_remove', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.CartRemove)

    def test_order_detail_url(self):
        url = reverse('orders:order_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.OrderDetailView)

    def test_order_remove_url(self):
        url = reverse('orders:order_remove', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.OrderRemoveView)

    def test_order_create_url(self):
        url = reverse('orders:order_create')
        self.assertEqual(resolve(url).func.view_class, views.OrderCreateView)

    def test_order_list_url(self):
        url = reverse('orders:order_list')
        self.assertEqual(resolve(url).func.view_class, views.OrderListView)






