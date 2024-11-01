from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Заказ {order.id}"
    message = (
        f"Уважаемый {order.first_name}," f"Ваш заказ был успешно создан!",
        f"Номер вашего заказа {order.id}",
    )
    mail_sent = send_mail(subject, message, "joystickgames@gmail.com", [order.email])
    return mail_sent
