from django.db import models
from django.contrib.auth import get_user_model
from category.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
import logging


User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        ordering = ['paid', '-updated']

    def __str__(self):
        return f"{str(self.user)} - {str(self.id)}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.order_items.all())
        if self.discount != 0 and self.discount != None:
            discount = total * self.discount // 100
            total = total - discount
        return total

    def get_items_count(self):
        return sum(item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def get_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

