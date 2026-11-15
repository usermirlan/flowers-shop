from django import forms

from .models import Product, ShopSettings


class StyledMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            w = f.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = "chk"
            elif not isinstance(w, forms.ClearableFileInput):
                w.attrs["class"] = "inp"


class ProductForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name_ky", "name_ru", "desc_ky", "desc_ru", "price", "badge", "image", "art", "art_colors", "is_active", "order"]


class SettingsForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = ShopSettings
        fields = ["name", "tagline_ky", "tagline_ru", "whatsapp", "phone", "instagram", "address", "hours", "map_url",
                  "delivery_fee", "free_delivery_from", "promo_title_ky", "promo_title_ru", "promo_date"]
        widgets = {"promo_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
