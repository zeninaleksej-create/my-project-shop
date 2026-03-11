from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Category, Product
from .forms import SearchForm, ServiceOrderForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product, 
        'cart_product_form': cart_product_form
    })

def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(Q(name__iregex=query) | Q(description__iregex=query))
    return render(request, 'shop/product/search.html', {
        'form': form,
        'query': query,
        'results': results
    })

def service_order_view(request):
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            subject = 'Новый заказ услуги'
            message = f"Email: {order.email}\nТелефон: {order.phone}\nОписание: {order.description}"
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['info@hlamstore.ru'])
            except:
                pass
            return redirect('shop:thanks_page')
    else:
        form = ServiceOrderForm()
    return render(request, 'shop/services.html', {'form': form})

def thanks_view(request):
    return render(request, 'shop/thanks.html')

def contacts(request):
    return render(request, 'shop/contacts.html')

def about(request):
    return render(request, 'shop/about.html')
