from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------------------------------
    # ОСНОВНІ ТА СТАТИЧНІ СТОРІНКИ
    # ----------------------------------------------------
    path('', views.home, name="home"),
    path('catalog/', views.store, name="store"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

    # ----------------------------------------------------
    # ФУНКЦІОНАЛ БЛОГУ (ВИПРАВЛЕНО)
    # ----------------------------------------------------
    path('blog/', views.blog_list, name="blog_list"), # Список статей
    path('blog/<slug:post_slug>/', views.blog_detail, name="blog_detail"), # Деталізація статті


    # ----------------------------------------------------
    # ФУНКЦІОНАЛЬНІ МАРШРУТИ КОШИКА
    # ----------------------------------------------------
    path('cart/', views.cart, name="cart"),

    # Маршрут оформлення (обробляє GET та POST)
    path('checkout/', views.checkout, name="checkout"),

    # КРИТИЧНИЙ МАРШРУТ: Сторінка успішного оформлення
    path('checkout/success/<int:order_id>/', views.checkout_success, name="checkout_success"),

    # AJAX оновлення кошика
    path('update_item/', views.updateItem, name="update_item"),
]