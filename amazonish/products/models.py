from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('name', 'parent_category', 'slug', 'tags',
                    'description', 'created_at', 'updated_at')


class Products(models.Model):
    category_id = models.ForeignKey(
        Category, related_name="product_cat", on_delete=models.CASCADE
    )
    title = models.TextField()
    picture = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    price = models.TextField()
    discount_type = models.TextField()
    discount_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    stocks = models.CharField(max_length=255,default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('category_id',  'title',
                    'picture',
                    'summary',
                    'description',
                    'price',
                    'discount_type',
                    'discount_value',
                    'created_at',
                    'updated_at', 'stocks')
