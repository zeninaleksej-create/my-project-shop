from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск')







from django import forms
from .models import ServiceOrder

class ServiceOrderForm(forms.ModelForm): # МЕНЯЕМ ТУТ
    class Meta:
        model = ServiceOrder
        fields = ['email', 'phone', 'description']


    email = forms.EmailField(
        label='Ваша почта', 
        widget=forms.EmailInput()
    )
    phone = forms.CharField(
        label='Телефон', 
        max_length=20, 
        widget=forms.TextInput()
    )
    description = forms.CharField(
        label='Описание пожелания', 
        widget=forms.Textarea(attrs={'rows': 5})
    )


from django.contrib import admin
from .models import ServiceOrder
