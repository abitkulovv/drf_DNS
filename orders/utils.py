from django.core.mail import send_mail
from django.conf import settings

def send_order_update_email(order):
    subject = f'Обновление заказа #{order.id}'
    message = f'Здравствуйте, {order.user.username}!\n\n'
    message += f'Статус вашего заказа изменён на: {order.status}\n\n'
    message += 'Спасибо за покупку!'
    recipient_list = [order.user.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)