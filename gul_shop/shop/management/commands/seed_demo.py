from django.core.management.base import BaseCommand

from shop.models import Category, Product, ShopSettings

CATS = [
    ("roses", "Розы", "Розалар"),
    ("tulips", "Тюльпаны", "Жоогазындар"),
    ("peonies", "Пионы", "Пиондор"),
    ("mix", "Букеты-микс", "Аралаш десте"),
    ("gifts", "Подарки", "Белектер"),
]

PRODUCTS = [
    ("roses", 3500, "hit", "rose", "#c8243b,#b01e33,#d6354b",
     "25 красных роз", "Классика: местные розы 60 см, крафт-упаковка",
     "25 кызыл роза", "Классика: 60 см жергиликтүү розалар, крафт кагаз"),
    ("roses", 6900, "", "rose", "#f2a7bb,#e889a3,#f7c4d1",
     "51 роза «Нежность»", "Розовые розы в шляпной коробке",
     "51 роза «Назиктик»", "Кызгылт розалар кутуда"),
    ("tulips", 1800, "new", "tulip", "#e6394d,#f4b52e,#ef7aa0,#f6f0e0",
     "15 тюльпанов микс", "Весенний микс из пяти цветов",
     "15 жоогазын микс", "Беш түстөгү жазгы аралаш"),
    ("peonies", 4500, "hit", "peony", "#f3a6bd,#f7c6d4,#e8839f",
     "Пионы «Облако»", "9 пышных пионов, сезонное предложение",
     "Пиондор «Булут»", "9 пиондон десте, мезгилдик сунуш"),
    ("mix", 2900, "", "mix", "#f2a7bb,#f4b52e,#ffffff,#c8243b",
     "Букет «Ош весна»", "Розы, хризантемы, эвкалипт",
     "«Ош жазы» дестеси", "Розалар, хризантемалар, эвкалипт"),
    ("mix", 1200, "", "daisy", "#ffffff",
     "Ромашки", "Летний букет из полевых ромашек",
     "Ромашкалар", "Талаа ромашкаларынан жайкы десте"),
    ("roses", 12900, "", "rose", "#c8243b,#a61b2e,#d6354b",
     "101 роза", "Для самого важного момента",
     "101 роза", "Эң маанилүү учур үчүн"),
    ("roses", 1700, "", "rose", "#fbf7f0,#efe6d6,#ffffff",
     "11 белых роз", "Нежно и элегантно",
     "11 ак роза", "Назик жана көрктүү"),
    ("gifts", 1500, "hit", "straw", "#e0263e",
     "Клубника в шоколаде", "12 ягод в подарочной коробке",
     "Шоколаддагы кулпунай", "Белек кутусунда 12 даана"),
    ("gifts", 4500, "new", "combo", "#f2a7bb,#c8243b,#ffffff",
     "Комбо: букет + клубника", "Розы и 9 ягод в шоколаде",
     "Комбо: десте + кулпунай", "Розалар жана шоколаддагы 9 кулпунай"),
]


class Command(BaseCommand):
    help = "Демо категорияларды жана товарларды кошот (бош базага гана)."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Товарлар бар болсо да кошуу")

    def handle(self, *args, **opts):
        ShopSettings.load()
        if Product.objects.exists() and not opts["force"]:
            self.stdout.write(self.style.WARNING("Товарлар бар экен, эч нерсе кошулган жок (--force менен кошсо болот)."))
            return
        cats = {}
        for i, (slug, ru, ky) in enumerate(CATS):
            cats[slug], _ = Category.objects.get_or_create(slug=slug, defaults={"name_ru": ru, "name_ky": ky, "order": i})
        for i, (cat, price, badge, art, colors, nru, dru, nky, dky) in enumerate(PRODUCTS):
            Product.objects.create(
                category=cats[cat], price=price, badge=badge, art=art, art_colors=colors,
                name_ru=nru, desc_ru=dru, name_ky=nky, desc_ky=dky, order=i,
            )
        self.stdout.write(self.style.SUCCESS(f"{len(PRODUCTS)} товар кошулду."))
