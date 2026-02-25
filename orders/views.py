from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created
from django.contrib.auth.decorators import login_required
from .models import Order

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. Создаем объект заказа, но НЕ сохраняем его в БД сразу
            order = form.save(commit=False)
            
            # 2. Если пользователь вошел, привязываем его к заказу
            if request.user.is_authenticated:
                order.user = request.user
            
            # 3. Теперь сохраняем заказ в базу данных
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # очистка корзины
            cart.clear()
            # запуск асинхронной задачи
            order_created(order.id)
            return render(
                request, 'orders/order/created.html', {'order': order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )




@login_required
def user_orders(request):
    # Мы просто фильтруем заказы по пользователю и сортируем их
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order/list.html', {'orders': orders})
