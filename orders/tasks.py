from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Заказ №{order.id}'
        
        # Контекст для шаблона (теперь товары ТОЧНО будут в базе)
        context = {'order': order}
        
        html_content = render_to_string('orders/order_email.html', context)
        text_content = strip_tags(html_content)
        
        # Отправка пользователю
        msg = EmailMultiAlternatives(
            subject, 
            text_content, 
            settings.DEFAULT_FROM_EMAIL, 
            [order.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Отправка администраторам (из settings.ADMINS)
        admin_emails = [addr for name, addr in settings.ADMINS]
        if admin_emails:
            admin_msg = EmailMultiAlternatives(
                f'НОВЫЙ ЗАКАЗ №{order.id}', 
                text_content, 
                settings.DEFAULT_FROM_EMAIL, 
                admin_emails
            )
            admin_msg.attach_alternative(html_content, "text/html")
            admin_msg.send()
            
        return True
    except Order.DoesNotExist:
        return False
