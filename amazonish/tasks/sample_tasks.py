from django.db.models import Manager
from products.models import Category, Products


class ProductsManager(Manager):
    def get_queryset(self):
        return Products.objects.raw('SELECT * FROM public.products_products')

    def get_stocks(self, num):
        string_stock = str(num)
        return Products.objects.raw("SELECT id, price, title, stocks FROM public.products_products WHERE stocks = %s", [string_stock])
