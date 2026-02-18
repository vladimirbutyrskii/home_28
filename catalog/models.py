from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание продукта"
    )
    photo = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        null=True,
        blank=True,
        related_name="products"
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену продукта")
    created_at = models.DateField(
        verbose_name="Дата создания", help_text="Введите дату создания продукта"
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения",
        help_text="Введите дату последнего изменения продукта",
        blank=True,
        null=True,
    )
    manufactured_at = models.DateField(
        verbose_name="Дата производства продукта",
        help_text="Введите дату производства продукта",
        blank=True,
        null=True,
    )

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0
    )

    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца продукта", blank=True,
                              null=True, on_delete=models.SET_NULL)

    new_item = models.BooleanField(
        verbose_name="Признак новинки",
        help_text="Введите признак новинки продукта",
        default=False
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product")
        ]


    def __str__(self):
        return self.name

