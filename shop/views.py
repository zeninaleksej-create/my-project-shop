from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Category, Product



from .forms import SearchForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        {'product': product, 'cart_product_form': cart_product_form},
    )






from django.db.models import Q  # Импортируйте Q
from django.shortcuts import render
from .models import Product
from .forms import SearchForm

def product_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Используем Q для поиска по названию ИЛИ описанию
            results = Product.objects.filter(Q(name__iregex=query) | Q(description__iregex=query))

    return render(request, 'shop/product/search.html', {
        'form': form,
        'query': query,
        'results': results
    })




def services(request):
    return render(request, 'shop/services.html')





from django.shortcuts import render
from .forms import ServiceOrderForm

def services(request):
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            # Здесь можно отправить письмо или сохранить в базу
            # Данные в form.cleaned_data['email'], и т.д.
            return render(request, 'shop/services.html', {'form': form, 'success': True})
    else:
        form = ServiceOrderForm()
    
    return render(request, 'shop/services.html', {'form': form})









from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ServiceOrderForm
from .models import ServiceRequest

def services(request):
    success = False
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем в базу данных
            data = form.cleaned_data
            ServiceRequest.objects.create(
                email=data['email'],
                phone=data['phone'],
                description=data['description']
            )
            
            # 2. Отправляем на почту
            subject = 'Новая заявка на услуги художественной студии'
            message = f"Почта: {data['email']}\nТелефон: {data['phone']}\nПожелания: {data['description']}"
            try:
                send_mail(subject, message, 'info@hlamstore.ru', ['info@hlamstore.ru'])
            except:
                pass # Если почта не настроена, сайт не упадет
            
            success = True
    else:
        form = ServiceOrderForm()
    
    return render(request, 'shop/services.html', {'form': form, 'success': success})


