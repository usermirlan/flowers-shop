import re
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


def validate_wa(value):
    digits = re.sub(r"\D", "", value or "")
    if not (11 <= len(digits) <= 15):
        raise ValidationError("Номерди өлкө коду менен жазыңыз, мисалы: 996700123456")


class ShopSettings(models.Model):
    """Дүкөндүн негизги маалыматы. Бир гана жазуу болот."""

    name = models.CharField("Дүкөндүн аты", max_length=80, default="Bloom")
    tagline_ru = models.CharField("Ураан (орусча)", max_length=120, default="Цветы, которые говорят за вас")
    tagline_ky = models.CharField("Ураан (кыргызча)", max_length=120, default="Сиздин сезимиңизди айткан гүлдөр")
    whatsapp = models.CharField(
        "WhatsApp номери", max_length=20, validators=[validate_wa],
        help_text="Буйрутмалар ушул номерге келет. Мисалы: 996700123456",
        default="996700000000",
    )
    phone = models.CharField("Телефон (көрсөтүү үчүн)", max_length=30, blank=True)
    instagram = models.CharField("Instagram (@сыз)", max_length=60, blank=True)
    address = models.CharField("Дарек", max_length=160, blank=True, default="г. Ош")
    hours = models.CharField("Иш убактысы", max_length=60, blank=True, default="08:00–22:00")
    map_url = models.URLField("2GIS шилтемеси", blank=True)
    delivery_fee = models.PositiveIntegerField("Жеткирүү баасы (сом)", default=200)
    free_delivery_from = models.PositiveIntegerField("Акысыз жеткирүү (сомдон)", default=5000)
    promo_title_ru = models.CharField("Акциянын аталышы (орусча)", max_length=80, blank=True, default="До 14 февраля осталось")
    promo_title_ky = models.CharField("Акциянын аталышы (кыргызча)", max_length=80, blank=True, default="14-февралга чейин калды")
    promo_date = models.DateField("Акциянын күнү", null=True, blank=True,
                                  help_text="Таймер ушул күнгө чейин санайт. Бош калса, таймер көрүнбөйт.")

    class Meta:
        verbose_name = "Дүкөндүн жөндөөлөрү"
        verbose_name_plural = "Дүкөндүн жөндөөлөрү"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @property
    def wa_digits(self):
        return re.sub(r"\D", "", self.whatsapp)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"promo_date": cls.next_valentine()})
        return obj

    @staticmethod
    def next_valentine():
        today = date.today()
        d = date(today.year, 2, 14)
        return d if d >= today else date(today.year + 1, 2, 14)


class Category(models.Model):
    name_ru = models.CharField("Аталышы (орусча)", max_length=60)
    name_ky = models.CharField("Аталышы (кыргызча)", max_length=60)
    slug = models.SlugField("Шилтеме аты (латынча)", unique=True)
    order = models.PositiveIntegerField("Тартиби", default=0)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ky


class Product(models.Model):
    BADGES = [("", "—"), ("hit", "Хит"), ("new", "Жаңы")]
    ART = [
        ("rose", "Роза"), ("tulip", "Жоогазын"), ("peony", "Пион"),
        ("mix", "Аралаш"), ("daisy", "Ромашка"), ("straw", "Кулпунай"), ("combo", "Комбо"),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    name_ru = models.CharField("Аталышы (орусча)", max_length=100)
    name_ky = models.CharField("Аталышы (кыргызча)", max_length=100)
    desc_ru = models.CharField("Кыскача (орусча)", max_length=200, blank=True)
    desc_ky = models.CharField("Кыскача (кыргызча)", max_length=200, blank=True)
    price = models.PositiveIntegerField("Баасы (сом)")
    image = models.ImageField("Сүрөтү", upload_to="products/", blank=True,
                              help_text="Чарчы сүрөт жакшы көрүнөт. Сүрөт жок болсо, тартылган гүл көрүнөт.")
    art = models.CharField("Сүрөт жок болгондо", max_length=10, choices=ART, default="rose")
    art_colors = models.CharField("Түстөрү (сүрөт жок болгондо)", max_length=80, default="#c8243b,#b01e33,#d6354b",
                                  help_text="Үтүр менен бөлүнгөн түстөр")
    badge = models.CharField("Белги", max_length=5, choices=BADGES, blank=True)
    is_active = models.BooleanField("Сайтта көрүнөт", default=True)
    order = models.PositiveIntegerField("Тартиби", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товарлар"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name_ky} — {self.price} сом"


class Order(models.Model):
    STATUS = [
        ("new", "Жаңы"), ("confirmed", "Ырасталды"), ("delivering", "Жолдо"),
        ("done", "Аткарылды"), ("cancelled", "Жокко чыгарылды"),
    ]
    created = models.DateTimeField("Түшкөн убакыт", auto_now_add=True)
    status = models.CharField("Абалы", max_length=12, choices=STATUS, default="new")
    delivery = models.BooleanField("Жеткирүү", default=True)
    date = models.DateField("Күнү")
    time_slot = models.CharField("Убактысы", max_length=20)
    address = models.CharField("Дарек", max_length=200, blank=True)
    recipient = models.CharField("Алуучу", max_length=80, blank=True)
    phone = models.CharField("Телефон", max_length=30)
    card_text = models.CharField("Открытка", max_length=300, blank=True)
    items_total = models.PositiveIntegerField("Товарлар (сом)", default=0)
    delivery_fee = models.PositiveIntegerField("Жеткирүү (сом)", default=0)
    total = models.PositiveIntegerField("Жалпы (сом)", default=0)
    lang = models.CharField(max_length=2, default="ru")

    class Meta:
        verbose_name = "Буйрутма"
        verbose_name_plural = "Буйрутмалар"
        ordering = ["-created"]

    def __str__(self):
        return f"№{self.pk} — {self.total} сом"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField("Аталышы", max_length=100)
    price = models.PositiveIntegerField("Баасы")
    qty = models.PositiveIntegerField("Саны")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Буйрутмадагы товарлар"

    @property
    def line_total(self):
        return self.price * self.qty
