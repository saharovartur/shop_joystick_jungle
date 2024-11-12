from django import forms
from localflavor.ru.forms import RUPostalCodeField

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма создания заказа
    """

    postal_code = RUPostalCodeField()

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
