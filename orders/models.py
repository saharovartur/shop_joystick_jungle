from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon
from shop.models import Product


class Order(models.Model):
    """Модель заказа"""

    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50, verbose_name="Фамилия")
    email = models.EmailField(
        _("email"),
    )
    address = models.CharField(_("address"), max_length=250, verbose_name="Адрес")
    postal_code = models.CharField(
        _("postal code"), max_length=20, verbose_name="Почтовый индекс"
    )
    city = models.CharField(_("city"), max_length=100, verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Оплачено")
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.id}"

    def get_total_cost(self):
        """
        Общая стоимость товаров в заказе
        """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        """
        Метод для возврата информ.панели платежа заказа
        на сайте stripe
        :return:
        """
        if not self.stripe_id:
            return ""
        if "_test_" in settings.STRIPE_SECRET_KEY:
            path = "/test/"  # путь Stripe до тестовых платежей
        else:
            path = "/"  # путь до реальных платежей
        return f"https://dashboard.stripe.com{path}payments/{self.stripe_id}"

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):
    """Модель для детальной инфо о заказе"""

    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
