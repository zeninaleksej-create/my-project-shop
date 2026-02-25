from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_emails(sender, instance, created, **kwargs):
    if created:
        # 1. Подготовка данных
        subject = f'Заказ №{instance.id} в магазине'
        to_customer = [instance.email]
        # Извлекаем только email-адреса из кортежа ADMINS
        to_admin = [addr for name, addr in settings.ADMINS]
        
        context = {'order': instance}
        
        # 2. Рендерим HTML (шаблон создадим ниже)
        html_content = render_to_string('orders/order_email.html', context)
        text_content = strip_tags(html_content)

        # 3. Отправка пользователю
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to_customer)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # 4. Отправка администраторам
        if to_admin:
            admin_msg = EmailMultiAlternatives(f'НОВЫЙ ЗАКАЗ №{instance.id}', text_content, settings.DEFAULT_FROM_EMAIL, to_admin)
            admin_msg.attach_alternative(html_content, "text/html")
            admin_msg.send()
