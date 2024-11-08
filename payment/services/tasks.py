from io import BytesIO

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Асинх. функция по отправке письма с
    уведомлением об успешной оплате заказа
    """
    order = Order.objects.get(id=order_id)

    subject = f"JoyStickJungleShop - Номер заказа {order.id}"
    message = "Ваша счет-фактура на вашу недавнюю покупку."
    email = EmailMessage(subject, message, "joystick303@email.com", [order.email])

    # Генерация PDF
    html = render_to_string("order/pdf.html", {"order": order})
    out = BytesIO()
    pisa_status = pisa.CreatePDF(html, out)

    # Крепим pdf к письму
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
    email.send()
