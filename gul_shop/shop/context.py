from .models import ShopSettings


def shop_settings(request):
    return {"shop": ShopSettings.load()}
