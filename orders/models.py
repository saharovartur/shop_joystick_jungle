from django.db import models


class Order(models.Model):
    """Модель заказа"""
    first_name = models.CharField(max_length=50,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=50,
                                 verbose_name='Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250,
                               verbose_name='Адрес')
    postal_code = models.CharField(max_length=20,
                                   verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100,
                            verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False,
                               verbose_name='Оплачено')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        """
        Общая стоимость товаров в заказе
        """
        return sum(item.get_cost() for item in self.items.all())


