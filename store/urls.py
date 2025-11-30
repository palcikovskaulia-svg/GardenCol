from django.urls import path
from . import views

urlpatterns = [
    # Новий маршрут для Головної сторінки (якщо вона відрізняється від каталогу)
    path('', views.home, name="home"),

    # Каталог (раніше був '/' або 'store')
    path('catalog/', views.store, name="store"),

    # Інші статичні сторінки
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),

    # Функціональні маршрути
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
]