from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Order, OrderItem, Product, ShopSettings

admin.site.site_header = "Гүл дүкөнү — башкаруу"
admin.site.site_title = "Гүл дүкөнү"
admin.site.index_title = "Башкы бет"


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Негизги", {"fields": ("name", "tagline_ru", "tagline_ky")}),
        ("Байланыш", {"fields": ("whatsapp", "phone", "instagram", "address", "hours", "map_url")}),
        ("Жеткирүү", {"fields": ("delivery_fee", "free_delivery_from")}),
        ("Акция таймери", {"fields": ("promo_title_ru", "promo_title_ky", "promo_date")}),
    )

    def has_add_permission(self, request):
        return not ShopSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_ky", "name_ru", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name_ru",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name_ky", "category", "price", "badge", "is_active", "order")
    list_display_links = ("thumb", "name_ky")
    list_editable = ("price", "is_active", "order")
    list_filter = ("category", "is_active", "badge")
    search_fields = ("name_ky", "name_ru")
    fieldsets = (
        (None, {"fields": ("category", "name_ky", "name_ru", "desc_ky", "desc_ru", "price", "badge", "is_active", "order")}),
        ("Сүрөт", {"fields": ("image", "art", "art_colors")}),
    )

    @admin.display(description="Сүрөт")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:8px">', obj.image.url)
        return "—"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("name", "price", "qty", "line_total")
    fields = ("name", "price", "qty", "line_total")
    can_delete = False

    @admin.display(description="Суммасы")
    def line_total(self, obj):
        return obj.line_total


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "status", "date", "time_slot", "phone", "total", "kind")
    list_editable = ("status",)
    list_filter = ("status", "delivery", "date")
    search_fields = ("phone", "recipient", "address")
    date_hierarchy = "date"
    inlines = [OrderItemInline]
    readonly_fields = ("created", "items_total", "delivery_fee", "total", "wa_link")
    fields = ("status", "created", "delivery", "date", "time_slot", "address", "recipient", "phone",
              "card_text", "items_total", "delivery_fee", "total", "wa_link")

    @admin.display(description="Түрү")
    def kind(self, obj):
        return "Жеткирүү" if obj.delivery else "Өзү алат"

    @admin.display(description="Кардарга жазуу")
    def wa_link(self, obj):
        import re
        digits = re.sub(r"\D", "", obj.phone)
        if not digits:
            return "—"
        return format_html('<a href="https://wa.me/{}" target="_blank">WhatsApp\'та жазуу</a>', digits)
