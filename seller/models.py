from django.db import models
from django.conf import settings
from django.utils.text import slugify

class CategoryModel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness if needed
            counter = 1
            original_slug = self.slug
            while CategoryModel.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('user', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while ProductModel.objects.filter(user=self.user, slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class OrderModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, blank=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')  # new
    product_name = models.CharField(max_length=255, blank=True)  # new
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # new
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding:  # Only set on first save (new order)
            if self.product:
                self.product_name = self.product.name
                self.product_price = self.product.price
                self.seller = getattr(self.product, 'user', None)

            if not self.total_price and self.product_price:
                self.total_price = self.product_price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.product_name} x{self.quantity}"


