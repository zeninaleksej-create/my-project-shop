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
        subject = f'Заказ №{instance.id} в магазине'
        to_customer = [instance.email]
        to_admin = [addr for name, addr in settings.ADMINS]
        
        html_content = render_to_string('orders/order_email.html', {'order': instance})
        text_content = strip_tags(html_content)

        def send_msg(subj, recipients):
            msg = EmailMultiAlternatives(subj, text_content, settings.DEFAULT_FROM_EMAIL, recipients)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        send_msg(subject, to_customer)
        if to_admin:
            send_msg(f'НОВЫЙ ЗАКАЗ №{instance.id}', to_admin)
