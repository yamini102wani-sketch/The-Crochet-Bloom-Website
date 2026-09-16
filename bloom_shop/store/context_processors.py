from django.conf import settings
from .models import Product

def site_settings(request):
    return {
        "SHOP_WHATSAPP_NUMBER": settings.SHOP_WHATSAPP_NUMBER,
        "SHOP_EMAIL": settings.SHOP_EMAIL,
        "SHOP_PHONE": settings.SHOP_PHONE,
        "SHOP_ADDRESS": settings.SHOP_ADDRESS,
    }

def cart_count(request):
    cart = request.session.get("cart", {})
    return {"cart_count": sum(int(v.get("qty", 1)) if isinstance(v, dict) else int(v) for v in cart.values())}
