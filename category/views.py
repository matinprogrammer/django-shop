from lib2to3.fixes.fix_input import context
from orders.forms import CartAddForm
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from category.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'category/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddForm()
        return context

