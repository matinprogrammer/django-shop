from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.CartAddView.as_view()),
    path('remove/<int:product_id>/', views.CartRemoveView.as_view()),
    path('', views.CartView.as_view()),
    path('get_total_price/', views.CartGetTotalPrice.as_view()),
]