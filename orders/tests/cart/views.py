from rest_framework.views import APIView
from rest_framework.response import Response
from orders.cart import Cart
from category.models import Product


class CartAddView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(pk=product_id)
        cart.add(product=product, quantity=int(request.data['quantity']))
        return Response('Done')

class CartRemoveView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(pk=product_id)
        cart.remove(product=product)
        return Response('Done')

class CartView(APIView):
    def get(self, request):
        cart = Cart(request)
        return Response('Done')

class CartGetTotalPrice(APIView):
    def get(self, request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        return Response(total_price)





