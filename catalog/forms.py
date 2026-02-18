from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ("views_counter",)

    lock_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def clean_name(self):
        product_name = self.cleaned_data["name"]
        name_list = product_name.split()
        for part_name in name_list:
            for part_name in self.lock_words:
                if part_name.lower() in product_name.lower():
                    raise ValidationError(f"В названии продукта не должно быть слова '{part_name}' ")

        return product_name

    def clean_description(self):
        description = self.cleaned_data["description"]
        description_list = description.split()
        for part_description in description_list:
            for part_description in self.lock_words:
                if part_description.lower() in description.lower():
                    raise ValidationError(f"В описании продукта не должно быть слова '{part_description}' ")

        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError(f"Цена продукта не может быть отрицательной!")

        return price


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("is_published",)
