from django.db import models
from django.contrib.auth import get_user_model
from category.models import Product


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
        return f"{self.user} - {str(self.id)}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.order_items.all())
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
