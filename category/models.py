from django.db import models
from django.urls import reverse

def product_directory_path(instance, filename):
    return f'products/{instance.slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    picture = models.ImageField(upload_to=product_directory_path, blank=True, null=True)
    available = models.BooleanField(default=True)
    count = models.PositiveSmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('category:product_detail', kwargs={'slug': self.slug})