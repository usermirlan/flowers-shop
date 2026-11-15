import json
from datetime import date, timedelta
from urllib.parse import unquote

from django.core.management import call_command
from django.test import TestCase

from .models import Order, Product, ShopSettings


class ShopTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        s = ShopSettings.load()
        s.whatsapp = "996555123456"
        s.save()
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()

    def products(self):
        r = self.client.get("/")
        return r.context["products_json"]

    def post(self, **over):
        p = Product.objects.get(name_ru="25 красных роз")
        body = {"lang": "ru", "items": {str(p.id): 2}, "delivery": True, "date": self.tomorrow,
                "time": "12:00–15:00", "phone": "+996 700 111 222", "address": "Ленина 1", "recipient": "Айгерим", "card": "С любовью"}
        body.update(over)
        return self.client.post("/order/", json.dumps(body), content_type="application/json")

    def test_index(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("25 красных роз", [p["ru"][0] for p in self.products()])

    def test_order_ok_uses_db_price(self):
        r = self.post().json()
        self.assertTrue(r["ok"])
        o = Order.objects.get(pk=r["order"])
        self.assertEqual(o.items_total, 7000)
        self.assertEqual(o.delivery_fee, 0)  # 7000 >= 5000
        self.assertEqual(o.total, 7000)
        self.assertTrue(r["wa_url"].startswith("https://wa.me/996555123456?text="))
        self.assertIn("Ленина 1", unquote(r["wa_url"]))

    def test_delivery_fee_below_threshold(self):
        p = Product.objects.get(name_ru="Ромашки")
        r = self.post(items={str(p.id): 1}).json()
        self.assertEqual(Order.objects.get(pk=r["order"]).total, 1400)

    def test_pickup_no_fee_no_address(self):
        p = Product.objects.get(name_ru="Ромашки")
        r = self.post(items={str(p.id): 1}, delivery=False, address="").json()
        self.assertTrue(r["ok"])
        self.assertEqual(Order.objects.get(pk=r["order"]).total, 1200)

    def test_rejects_bad_input(self):
        self.assertEqual(self.post(address="").status_code, 400)
        self.assertEqual(self.post(date="2000-01-01").status_code, 400)
        self.assertEqual(self.post(time="25:00").status_code, 400)
        self.assertEqual(self.post(items={"99999": 1}).status_code, 400)
        self.assertEqual(self.post(items={}).status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_inactive_product_hidden_and_rejected(self):
        p = Product.objects.get(name_ru="Ромашки")
        p.is_active = False
        p.save()
        self.assertNotIn("Ромашки", [x["ru"][0] for x in self.products()])
        self.assertEqual(self.post(items={str(p.id): 1}).status_code, 400)

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        r = c.post("/order/", "{}", content_type="application/json")
        self.assertEqual(r.status_code, 403)


class OwnerPanelTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        call_command("seed_demo", verbosity=0)
        self.u = User.objects.create_user("owner", password="Gul-test-123", is_staff=True)

    def test_requires_login(self):
        r = self.client.get("/owner/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/owner/login/", r["Location"])

    def test_pages_and_actions(self):
        self.client.login(username="owner", password="Gul-test-123")
        for url in ["/owner/", "/owner/orders/", "/owner/orders/?s=all", "/owner/products/", "/owner/products/new/", "/owner/settings/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        p = Product.objects.first()
        self.client.post(f"/owner/products/{p.id}/price/", {"price": "999"})
        p.refresh_from_db()
        self.assertEqual(p.price, 999)
        self.client.post(f"/owner/products/{p.id}/toggle/")
        p.refresh_from_db()
        self.assertFalse(p.is_active)
        o = Order.objects.create(date=date.today(), time_slot="09:00–12:00", phone="+996700111222", total=100)
        self.client.post(f"/owner/orders/{o.id}/status/", {"status": "confirmed"})
        o.refresh_from_db()
        self.assertEqual(o.status, "confirmed")
        self.assertEqual(self.client.get("/owner/").status_code, 200)

    def test_non_staff_blocked(self):
        from django.contrib.auth.models import User
        User.objects.create_user("x", password="Gul-test-123")
        self.client.login(username="x", password="Gul-test-123")
        self.assertEqual(self.client.get("/owner/").status_code, 302)
