import os
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['id']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
"""
class ServiceRequest(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.email} - {self.created_at.strftime('%d.%m.%Y')}"
"""
class ServiceOrder(models.Model):
    email = models.EmailField(verbose_name='Ваша почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    description = models.TextField(verbose_name='Описание пожелания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return f"Заказ от {self.email} - {self.created_at.strftime('%d.%m.%Y')}"

@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
