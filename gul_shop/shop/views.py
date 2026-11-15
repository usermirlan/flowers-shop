import json
import re
from datetime import date, datetime
from urllib.parse import quote

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Category, Order, OrderItem, Product, ShopSettings

SLOTS = ["09:00–12:00", "12:00–15:00", "15:00–18:00", "18:00–21:00"]

MSG = {
    "ru": {"head": "Здравствуйте! Хочу оформить заказ №{n}:", "del": "Доставка", "pick": "Самовывоз",
           "date": "Дата и время", "addr": "Адрес", "rcp": "Получатель", "ph": "Телефон",
           "card": "Открытка", "tot": "Итого", "som": "сом"},
    "ky": {"head": "Саламатсызбы! №{n} буйрутма бергим келет:", "del": "Жеткирүү", "pick": "Өзүм алам",
           "date": "Күнү жана убактысы", "addr": "Дарек", "rcp": "Алуучу", "ph": "Телефон",
           "card": "Открытка", "tot": "Жалпы", "som": "сом"},
}


def fmt(n):
    return f"{n:,}".replace(",", " ")


def index(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    cats = Category.objects.filter(products__is_active=True).distinct()
    data = [
        {
            "id": p.id, "cat": p.category.slug, "price": p.price, "badge": p.badge,
            "img": p.image.url if p.image else "",
            "art": {"t": p.art, "c": [c.strip() for c in p.art_colors.split(",") if c.strip()]},
            "ru": [p.name_ru, p.desc_ru], "ky": [p.name_ky, p.desc_ky],
        }
        for p in products
    ]
    cat_data = [{"slug": c.slug, "ru": c.name_ru, "ky": c.name_ky} for c in cats]
    return render(request, "shop/index.html", {
        "products_json": data, "cats_json": cat_data, "slots_json": SLOTS,
    })


def _err(msg, status=400):
    return JsonResponse({"ok": False, "error": msg}, status=status)


@require_POST
def place_order(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return _err("bad_json")

    lang = body.get("lang") if body.get("lang") in MSG else "ru"
    items = body.get("items") or {}
    if not isinstance(items, dict) or not items:
        return _err("empty")

    delivery = bool(body.get("delivery", True))
    phone = str(body.get("phone", "")).strip()[:30]
    address = str(body.get("address", "")).strip()[:200]
    recipient = str(body.get("recipient", "")).strip()[:80]
    card = str(body.get("card", "")).strip()[:300]
    slot = str(body.get("time", ""))
    try:
        d = datetime.strptime(str(body.get("date", "")), "%Y-%m-%d").date()
    except ValueError:
        return _err("date")

    if d < date.today() or slot not in SLOTS or len(re.sub(r"\D", "", phone)) < 9:
        return _err("required")
    if delivery and not address:
        return _err("required")

    # Бааны кардардын браузеринен эмес, базадан алабыз
    lines = []
    for pid, qty in items.items():
        try:
            pid, qty = int(pid), int(qty)
        except (TypeError, ValueError):
            return _err("item")
        if not (1 <= qty <= 99):
            return _err("item")
        p = Product.objects.filter(pk=pid, is_active=True).first()
        if not p:
            return _err("item")
        lines.append((p, qty))

    shop = ShopSettings.load()
    items_total = sum(p.price * q for p, q in lines)
    fee = 0 if (not delivery or items_total >= shop.free_delivery_from) else shop.delivery_fee

    with transaction.atomic():
        order = Order.objects.create(
            delivery=delivery, date=d, time_slot=slot, address=address if delivery else "",
            recipient=recipient if delivery else "", phone=phone, card_text=card,
            items_total=items_total, delivery_fee=fee, total=items_total + fee, lang=lang,
        )
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=p, name=p.name_ru if lang == "ru" else p.name_ky, price=p.price, qty=q)
            for p, q in lines
        ])

    m = MSG[lang]
    txt = [m["head"].format(n=order.pk), ""]
    for p, q in lines:
        name = p.name_ru if lang == "ru" else p.name_ky
        txt.append(f"• {name} × {q} — {fmt(p.price * q)} {m['som']}")
    txt += ["", m["del"] if delivery else m["pick"], f"{m['date']}: {d.strftime('%d.%m.%Y')}, {slot}"]
    if delivery:
        txt.append(f"{m['addr']}: {address}")
        if recipient:
            txt.append(f"{m['rcp']}: {recipient}")
    txt.append(f"{m['ph']}: {phone}")
    if card:
        txt.append(f"{m['card']}: «{card}»")
    txt += ["", f"{m['tot']}: {fmt(order.total)} {m['som']}"]
    message = "\n".join(txt)

    return JsonResponse({
        "ok": True, "order": order.pk, "message": message,
        "wa_url": f"https://wa.me/{shop.wa_digits}?text={quote(message)}",
    })
