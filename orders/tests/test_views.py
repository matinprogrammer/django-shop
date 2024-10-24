from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model
from orders import models as order_models
from orders.models import Order

User = get_user_model()

credential = {
    'phone_number': '09000000000',
    'password': 'test_pass'
}
def create_user():
    return User.objects.create_user(
        **credential,
        first_name='test',
    )

class TestOrderListView(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_order_list_GET(self):
        self.client.login(**credential)
        response = self.client.get(reverse('orders:order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')


class TestOrderDetailView(TestCase):
    def setUp(self):
        self.user = create_user()
        self.order = baker.make(order_models.Order)
        self.order_item = baker.make(order_models.OrderItem, order=self.order)

    def test_order_list_GET(self):
        self.client.login(**credential)
        response = self.client.get(reverse('orders:order_detail', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertEqual(response.context['order'], self.order)
        # TODO: this code have error
        # self.assertEqual(response.context['order_items'], self.order.order_items.all())

class TestOrderCreateView(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_order_create_GET(self):
        self.client.login(**credential)
        response = self.client.get(reverse('orders:order_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:order_detail', args=[1]))
        self.assertEqual(order_models.Order.objects.all().count(), 1)

class TestOrderRemoveView(TestCase):
    def setUp(self):
        self.user = create_user()
        baker.make(order_models.Order)

    def test_order_remove_GET(self):
        self.client.login(**credential)
        response = self.client.get(reverse('orders:order_remove', args=[1]))

        self.assertEqual(response.status_code, 200)

class TestCartView(TestCase):
    def test_cart_view_GET(self):
        response = self.client.get(reverse('orders:cart'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/cart.html')
        self.failUnless(response.context['cart'])


class TestCartAddView(TestCase):
    def setUp(self):
        product = baker.make(order_models.Product)

    def test_cart_add_POST(self):
        response = self.client.post(reverse('orders:cart_add', args=[1]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:cart'))


class TestCartRemoveView(TestCase):
    def setUp(self):
        product = baker.make(order_models.Product)

    def test_cart_add_POST(self):
        response = self.client.post(reverse('orders:cart_add', args=[1]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:cart'))

