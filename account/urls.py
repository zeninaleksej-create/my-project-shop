from django.urls import path
from . import views

urlpatterns = [
    # ... ваши другие пути ...
    path('', views.register, name='register'),
]
