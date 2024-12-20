from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    """Модель категории"""

    translations = TranslatedFields(
        name=models.CharField(verbose_name="Название", max_length=100),
        slug=models.SlugField(max_length=200, unique=True),
    )

    class Meta:
        # ordering = ["name"]
        # indexes = [
        #   models.Index(
        #           fields=["name"],
        #  )
        # ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(TranslatableModel):
    """Модель товара"""

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )

    translations = TranslatedFields(
        name=models.CharField(max_length=200, verbose_name="Название"),
        slug=models.SlugField(max_length=200),
        description=models.TextField(blank=True, verbose_name="Описание"),
    )

    image = models.ImageField(
        upload_to="products/%Y/%m/%d", verbose_name="Изображение", blank=True
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="Наличие")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        # ordering = ["name"]
        indexes = [
            #   models.Index(fields=["id", "slug"]),
            #  models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
