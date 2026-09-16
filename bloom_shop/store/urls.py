from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("prices/", views.prices, name="prices"),
    path("about/", views.about, name="about"),
    path("reviews/", views.reviews, name="reviews"),
    path("contact/", views.contact, name="contact"),
    path("custom-order/", views.custom_order, name="custom_order"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/<str:order_id>/", views.order_success, name="order_success"),
    path("whatsapp/order/<str:order_id>/", views.whatsapp_order, name="whatsapp_order"),
    path("whatsapp/product/<slug:slug>/", views.whatsapp_product, name="whatsapp_product"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reviews/add/<int:product_id>/", views.add_review, name="add_review"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
