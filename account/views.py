



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail  # Добавляем импорт
from django.conf import settings         # Добавляем настройки
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            
            send_mail(
                'Новый пользователь на сайте',
                f'Зарегистрировался новый красавчик: {new_user.username} ({new_user.email})',
                settings.DEFAULT_FROM_EMAIL,
                ['info@hlamstore.ru'],
                fail_silently=False,
            )
            
            login(request, new_user)
            return redirect('shop:product_list') 
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})
