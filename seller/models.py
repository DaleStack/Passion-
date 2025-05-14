from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
# Create your models here.

class CategoryModel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ProductModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True)

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

    

