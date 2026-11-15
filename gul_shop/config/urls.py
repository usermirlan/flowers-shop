from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views

from shop import owner, views

urlpatterns = [
    path("", views.index, name="index"),
    path("order/", views.place_order, name="place_order"),
    path("owner/login/", owner.OwnerLogin.as_view(), name="owner_login"),
    path("owner/logout/", auth_views.LogoutView.as_view(next_page="owner_login"), name="owner_logout"),
    path("owner/", owner.dashboard, name="owner_dash"),
    path("owner/orders/", owner.orders, name="owner_orders"),
    path("owner/orders/<int:pk>/status/", owner.order_status, name="owner_order_status"),
    path("owner/products/", owner.products, name="owner_products"),
    path("owner/products/new/", owner.product_edit, name="owner_product_add"),
    path("owner/products/<int:pk>/", owner.product_edit, name="owner_product_edit"),
    path("owner/products/<int:pk>/toggle/", owner.product_toggle, name="owner_product_toggle"),
    path("owner/products/<int:pk>/price/", owner.product_price, name="owner_product_price"),
    path("owner/settings/", owner.settings_view, name="owner_settings"),
    path("panel/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
