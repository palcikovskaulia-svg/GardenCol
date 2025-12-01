from django.urls import path
from . import views

urlpatterns = [
    # Нові основні сторінки
    path('', views.home, name="home"),
    path('catalog/', views.store, name="store"),
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),

    # ----------------------------------------------------
    # Функціональні маршрути
    # ----------------------------------------------------

    path('cart/', views.cart, name="cart"),

    # Маршрут оформлення (обробляє GET та POST)
    path('checkout/', views.checkout, name="checkout"),

    # КРИТИЧНИЙ МАРШРУТ: Сторінка успішного оформлення
    path('checkout/success/<int:order_id>/', views.checkout_success, name="checkout_success"),

    path('update_item/', views.updateItem, name="update_item"),
]