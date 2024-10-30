from django.test import TestCase, override_settings
from orders.cart import Cart, CART_SESSION_KEY
from category.models import Product
from model_bakery import baker


@override_settings(ROOT_URLCONF='orders.tests.cart.urls')
class TestCartClass(TestCase):
    def setUp(self):
        self.product_1 = baker.make(Product, price=15)
        self.product_2 = baker.make(Product, price=20)

    def test_cart_add(self):
        response = self.client.post('/add/1/', data={'quantity': 1})
        my_session = response.client.session[CART_SESSION_KEY]
        self.assertEqual(my_session, {'1': {'quantity': 1}})

    def test_cart_add_dublicate(self):
        self.client.post('/add/1/', data={'quantity': 1})
        response = self.client.post('/add/1/', data={'quantity': 2})
        my_session = response.client.session[CART_SESSION_KEY]
        self.assertEqual(my_session, {'1': {'quantity': 3}})

    def test_cart_add_two_product(self):
        self.client.post('/add/1/', data={'quantity': 1})
        response = self.client.post('/add/2/', data={'quantity': 2})
        my_session = response.client.session[CART_SESSION_KEY]
        self.assertEqual(my_session, {'1': {'quantity': 1}, '2': {'quantity': 2}})

    def test_cart_add_does_not_exist(self):
        with self.assertRaises(Product.DoesNotExist):
            self.client.post('/add/3/', data={'quantity': 1})

    def test_cart_remove(self):
        my_session = self.client.session
        my_session[CART_SESSION_KEY] = {'1': {'quantity': 1}}
        my_session.save()
        response = self.client.post('/remove/1/')

        response_session = response.client.session[CART_SESSION_KEY]
        self.assertEqual(response_session, {})

    def test_cart_remove_secend_with_two_element(self):
        my_session = self.client.session
        my_session[CART_SESSION_KEY] = {'1': {'quantity': 1}, '2': {'quantity': 2}}
        my_session.save()
        response = self.client.post('/remove/2/')

        response_session = response.client.session[CART_SESSION_KEY]
        self.assertEqual(response_session, {'1': {'quantity': 1}})

    def test_cart_remove_does_not_exist(self):
        my_session = self.client.session
        my_session[CART_SESSION_KEY] = {'1': {'quantity': 1}, '2': {'quantity': 2}}
        my_session.save()
        with self.assertRaises(Product.DoesNotExist):
            self.client.post('/remove/3/')


    def test_cart_get_total_price(self):
        my_session = self.client.session
        my_session[CART_SESSION_KEY] = {'1': {'quantity': 3}, '2': {'quantity': 2}}
        my_session.save()
        response = self.client.get('/get_total_price/')
        self.assertEqual(response.data, 85)



@override_settings(ROOT_URLCONF='orders.tests.cart.urls')
class TestCartSpetialMethod(TestCase):
    def setUp(self):
        my_session = self.client.session
        my_session[CART_SESSION_KEY] = {'1': {'quantity': 1}, '2': {'quantity': 2}}
        my_session.save()
        response = self.client.post('/')
        self.response_session = response.client.session[CART_SESSION_KEY]

    def test_cart_iter(self):
        self.assertTrue(hasattr(self.response_session, '__iter__'))

    def test_cart_len(self):
        self.assertTrue(hasattr(self.response_session, '__len__'))


