from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    """
    Модель для хранения промо-кодов
    """

    code = models.CharField(max_length=50, unique=True, verbose_name="Код")
    valid_from = models.DateTimeField(verbose_name="От")
    valid_to = models.DateTimeField(verbose_name="Годен до")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Процентное значение (от 0 до 100)",
        verbose_name="Скидка",
    )
    active = models.BooleanField()

    def __str__(self):
        return self.code
