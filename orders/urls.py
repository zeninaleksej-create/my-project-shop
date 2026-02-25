from django.urls import path

from . import views


app_name = 'orders'


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    # Добавьте эту строку:
    path('my-orders/', views.user_orders, name='user_orders'),
]
