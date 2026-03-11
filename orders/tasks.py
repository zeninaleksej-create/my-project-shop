from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

def order_created(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Заказ №{order.id}'
        html_content = render_to_string('orders/order_email.html', {'order': order})
        text_content = strip_tags(html_content)
        admin_emails = [addr for name, addr in settings.ADMINS]

        def send_email(subj, recipients):
            msg = EmailMultiAlternatives(subj, text_content, settings.DEFAULT_FROM_EMAIL, recipients)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        send_email(subject, [order.email])
        if admin_emails:
            send_email(f'НОВЫЙ ЗАКАЗ №{order.id}', admin_emails)
        return True
    except Order.DoesNotExist:
        return False
