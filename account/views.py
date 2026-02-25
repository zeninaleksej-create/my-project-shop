

from django.shortcuts import render, redirect
from django.contrib.auth import login  # Импортируем функцию входа
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            # Автоматическая авторизация
            login(request, new_user)
            
            # Перенаправляем на главную страницу магазина или в личный кабинет
            return redirect('shop:product_list') 
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})
