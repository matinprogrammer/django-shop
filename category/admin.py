from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'count', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    raw_id_fields = ('category',)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name', 'created')
