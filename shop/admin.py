from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}





from .models import ServiceRequest


from django.contrib import admin
from .models import ServiceOrder  # Импортируй свою модель

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    # Эти колонки будут видны в списке в админке
    list_display = ('email', 'phone', 'created_at')
    # Добавим фильтр по дате для удобства
    list_filter = ('created_at',)
