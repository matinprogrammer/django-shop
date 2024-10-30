from venv import logger

from django.test import TestCase
from orders import models as orders_models
from accounts import models as accounts_models
from category import models as category_models
from model_bakery import baker


class TestOrderModel(TestCase):
    def setUp(self):
        user = baker.make(accounts_models.User, phone_number='09000000000')
        self.order = baker.make(orders_models.Order, user=user)

        product_1 = baker.make(category_models.Product, price=10)
        product_2 = baker.make(category_models.Product, price=15)
        baker.make(orders_models.OrderItem,order=self.order, product=product_1, quantity=2)
        baker.make(orders_models.OrderItem,order=self.order, product=product_2, quantity=4)

    def test_model_str(self):
        self.assertEqual(str(self.order), '09000000000 - 1')

    def test_get_total_price(self):
        self.assertEqual(self.order.get_total_price(), 80)

    def test_get_total_price_with_discount(self):
        self.order.discount=50
        self.assertEqual(self.order.get_total_price(), 40)

    def test_get_items_count(self):
        self.assertEqual(self.order.get_items_count(), 6)


class TestOrderItemModel(TestCase):
    def setUp(self):
        product = baker.make(category_models.Product, price=15, name='product-name')
        self.order_item = baker.make(orders_models.OrderItem, product=product, quantity=4)

    def test_model_str(self):
        self.assertEqual(str(self.order_item), 'product-name - 4')

    def test_get_cost(self):
        self.assertEqual(self.order_item.get_cost(), 60)


class TestCouponModel(TestCase):
    def setUp(self):
        self.coupon = baker.make(orders_models.Coupon, code=123456)

    def test_model_str(self):
        self.assertEqual(str(self.coupon), '123456')




