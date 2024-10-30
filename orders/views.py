from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CartAddForm, CouponApplyForm
from category.models import Product
from .cart import Cart
from .models import Order, OrderItem, Coupon
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib import messages



class OrderListView(LoginRequiredMixin, View):
    template_name = 'orders/orders.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        return render(request, self.template_name, {'orders': orders})

class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order_detail.html'
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order_items = order.order_items.all()

        return render(request, self.template_name, {
            'order': order,
            'order_items': order_items,
            'form': self.form_class,
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


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exists', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)


# MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
# CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

# class OrderPayView(LoginRequiredMixin, View):
#     def get(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         request.session['order_pay'] = {
#             'order_id': order.id,
#         }
#         req_data = {
#             "merchant_id": MERCHANT,
#             "amount": order.get_total_price(),
#             "callback_url": CallbackURL,
#             "description": description,
#             "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
#         }
#         req_header = {"accept": "application/json",
#                       "content-type": "application/json'"}
#         req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
#             req_data), headers=req_header)
#         authority = req.json()['data']['authority']
#         if len(req.json()['errors']) == 0:
#             return redirect(ZP_API_STARTPAY.format(authority=authority))
#         else:
#             e_code = req.json()['errors']['code']
#             e_message = req.json()['errors']['message']
#             return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#
#
# class OrderVerifyView(LoginRequiredMixin, View):
#     def get(self, request):
#         order_id = request.session['order_pay']['order_id']
#         order = Order.objects.get(id=int(order_id))
#         t_status = request.GET.get('Status')
#         t_authority = request.GET['Authority']
#         if request.GET.get('Status') == 'OK':
#             req_header = {"accept": "application/json",
#                           "content-type": "application/json'"}
#             req_data = {
#                 "merchant_id": MERCHANT,
#                 "amount": order.get_total_price(),
#                 "authority": t_authority
#             }
#             req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
#             if len(req.json()['errors']) == 0:
#                 t_status = req.json()['data']['code']
#                 if t_status == 100:
#                     order.paid = True
#                     order.save()
#                     return HttpResponse('Transaction success.\nRefID: ' + str(
#                         req.json()['data']['ref_id']
#                     ))
#                 elif t_status == 101:
#                     return HttpResponse('Transaction submitted : ' + str(
#                         req.json()['data']['message']
#                     ))
#                 else:
#                     return HttpResponse('Transaction failed.\nStatus: ' + str(
#                         req.json()['data']['message']
#                     ))
#             else:
#                 e_code = req.json()['errors']['code']
#                 e_message = req.json()['errors']['message']
#                 return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#         else:
#             return HttpResponse('Transaction failed or canceled by user')