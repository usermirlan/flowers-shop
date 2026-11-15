"""Дүкөн ээсинин кооз панели: /owner/"""
from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ProductForm, SettingsForm
from .models import Order, Product, ShopSettings

owner_required = staff_member_required(login_url="owner_login")


class OwnerLogin(auth_views.LoginView):
    template_name = "shop/owner/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or "/owner/"


def _counts():
    return {"new_orders": Order.objects.filter(status="new").count()}


@owner_required
def dashboard(request):
    today = timezone.localdate()
    week_ago = today - timedelta(days=6)
    valid = ~Q(status="cancelled")
    today_qs = Order.objects.filter(created__date=today).filter(valid)
    week_qs = Order.objects.filter(created__date__gte=week_ago).filter(valid)

    # Акыркы 7 күндүн графиги
    days = []
    rows = {r["d"]: r for r in week_qs.annotate(d=TruncDate("created")).values("d").annotate(n=Count("id"), s=Sum("total"))}
    peak = max([r["s"] or 0 for r in rows.values()] + [1])
    for i in range(7):
        d = week_ago + timedelta(days=i)
        r = rows.get(d) or {"n": 0, "s": 0}
        days.append({"label": d.strftime("%d.%m"), "n": r["n"], "s": r["s"] or 0, "h": int((r["s"] or 0) / peak * 100)})

    upcoming = Order.objects.filter(date__gte=today, status__in=["new", "confirmed", "delivering"]).order_by("date", "time_slot")[:8]
    top = (Product.objects.filter(orderitem__order__created__date__gte=today - timedelta(days=30))
           .exclude(orderitem__order__status="cancelled")
           .annotate(sold=Sum("orderitem__qty")).order_by("-sold")[:5])
    return render(request, "shop/owner/dashboard.html", {
        "tab": "dash", **_counts(),
        "today_n": today_qs.count(), "today_sum": today_qs.aggregate(s=Sum("total"))["s"] or 0,
        "week_n": week_qs.count(), "week_sum": week_qs.aggregate(s=Sum("total"))["s"] or 0,
        "days": days, "upcoming": upcoming, "top": top,
    })


@owner_required
def orders(request):
    st = request.GET.get("s", "active")
    qs = Order.objects.prefetch_related("items")
    if st == "active":
        qs = qs.filter(status__in=["new", "confirmed", "delivering"])
    elif st in dict(Order.STATUS):
        qs = qs.filter(status=st)
    return render(request, "shop/owner/orders.html", {
        "tab": "orders", **_counts(), "orders": qs[:100], "st": st, "statuses": Order.STATUS,
    })


@owner_required
@require_POST
def order_status(request, pk):
    o = get_object_or_404(Order, pk=pk)
    s = request.POST.get("status")
    if s in dict(Order.STATUS):
        o.status = s
        o.save(update_fields=["status"])
        messages.success(request, f"№{o.pk} буйрутма: {o.get_status_display()}")
    return redirect(request.POST.get("next") or "owner_orders")


@owner_required
def products(request):
    return render(request, "shop/owner/products.html", {
        "tab": "products", **_counts(), "products": Product.objects.select_related("category"),
    })


@owner_required
def product_edit(request, pk=None):
    p = get_object_or_404(Product, pk=pk) if pk else None
    form = ProductForm(request.POST or None, request.FILES or None, instance=p)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        messages.success(request, f"«{obj.name_ky}» сакталды")
        return redirect("owner_products")
    return render(request, "shop/owner/product_form.html", {"tab": "products", **_counts(), "form": form, "p": p})


@owner_required
@require_POST
def product_toggle(request, pk):
    p = get_object_or_404(Product, pk=pk)
    p.is_active = not p.is_active
    p.save(update_fields=["is_active"])
    return redirect("owner_products")


@owner_required
@require_POST
def product_price(request, pk):
    p = get_object_or_404(Product, pk=pk)
    try:
        price = int(request.POST.get("price", ""))
        if price < 0:
            raise ValueError
    except ValueError:
        messages.error(request, "Баа туура эмес")
    else:
        p.price = price
        p.save(update_fields=["price"])
        messages.success(request, f"«{p.name_ky}»: {price} сом")
    return redirect("owner_products")


@owner_required
def settings_view(request):
    form = SettingsForm(request.POST or None, instance=ShopSettings.load())
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Жөндөөлөр сакталды")
        return redirect("owner_settings")
    return render(request, "shop/owner/settings.html", {"tab": "settings", **_counts(), "form": form})
