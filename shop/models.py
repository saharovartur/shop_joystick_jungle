from django.db import models


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(verbose_name='Название',
                            max_length=100,)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'],)
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              verbose_name='Изображение',
                              blank=True)
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    available = models.BooleanField(default=True,
                                    verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Обновлено')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

