from django import forms
from .models import ServiceOrder

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск')

class ServiceOrderForm(forms.ModelForm):
    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput())
    phone = forms.CharField(label='Телефон', max_length=20, widget=forms.TextInput())
    description = forms.CharField(label='Описание пожелания', widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = ServiceOrder
        fields = ['email', 'phone', 'description']
