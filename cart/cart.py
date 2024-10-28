from django.conf import settings


class Cart:
    def __init__(self, request):
        """
        Инициализация корзины

        :param request: текущий запрос
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)  # Получаем корзину из текущего сеанса

        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Добавляет продукт в корзину или обновляет существующий продукт.

        :param product: объект товара
        :param quantity: кол-во товара (по умолчанию - 1)
        :param override_quantity: Перезаписать кол-во товара
        :return: None
        """
        product_id = str(product.id)  # конвертируем в str из-за особенностей работы
                                      # сериализации сеансовых данных через JSON
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True  # Помечаем сеанс как "измененный"
                                      # чтобы обеспечить его сохранение



