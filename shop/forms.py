from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск')





class ServiceOrderForm(forms.Form):
    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'}))
    phone = forms.CharField(label='Телефон', max_length=20, widget=forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}))
    description = forms.CharField(
        label='Описание пожелания', 
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Опишите ваши идеи для заказа...'})
    )
