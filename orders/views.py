from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CartAddForm
from category.models import Product
from .cart import Cart
from .models import Order, OrderItem
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderListView(LoginRequiredMixin, View):
    template_name = 'orders/orders.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        return render(request, self.template_name, {'orders': orders})

class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order_detail.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order_items = order.order_items.all()

        return render(request, self.template_name, {
            'order': order,
            'order_items': order_items,
        })

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('orders:order_detail', order.id)

class OrderRemoveView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:order_list')
    pk_url_kwarg = 'order_id'
    template_name = 'orders/delete.html'

class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(View):
    form_class = CartAddForm

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemove(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.remove(product)
        return redirect('orders:cart')