from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


# Класс для управления корзиной


class Cart:
    def __init__(self, request):
        """
        Инициализация корзины

        :param request: текущий запрос
        """

        self.session = request.session
        cart = self.session.get(
            settings.CART_SESSION_ID
        )  # Получаем корзину из текущего сеанса

        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get(
            "coupon_id"
        )  # Сохранить текущий примененный купон

    def add(self, product, quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Добавляет продукт в корзину или обновляет существующий продукт.

        :param product: объект товара
        :param quantity: кол-во товара (по умолчанию:  1)
        :param override_quantity: Перезаписать кол-во товара
        :return: None
        """
        product_id = str(product.id)  # конвертируем в str из-за особенностей работы
        # сериализации сеансовых данных через JSON
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity

        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True  # Помечаем сеанс как "измененный"
        # чтобы обеспечить его сохранение

    def remove(self, product) -> None:
        """
        Удаление товара из корзины

        :param product: объект товара
        :return: None
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Прокрутить товары в корзине в цикле
        и получить товары из базы данных
        """
        product_ids = self.cart.keys()  # Получаем ключи словаря корзины
        products = Product.objects.filter(
            id__in=product_ids
        )  # Получить объекты product и добавить их в корзину
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Подсчет кол-ва товаров в корзине

        :return: кол-во товаров в корзине
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Общая стоимость товаров в корзине

        :return: общая стоимость покупки
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """
        Метод возврата объекта промо-кода
        :return: None
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Метод для подсчета суммы скидки
        :return: int
        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        Метода возврата суммы после скидки
        :return: int
        """
        return self.get_total_price() - self.get_discount()



