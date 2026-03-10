from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('services/', views.service_order_view, name='services'),
    path('thanks/', views.thanks_view, name='thanks_page'),
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category',),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail', ),
    
]