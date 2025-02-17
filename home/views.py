from django.shortcuts import render
from django.views import View
from category.models import Product


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        products = Product.objects.all()
        response = render(request, self.template_name, context={'products': products})
        return response

