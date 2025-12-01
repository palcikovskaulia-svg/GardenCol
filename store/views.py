from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product, Order, OrderItem
from django.db.models import Sum  # Додано для оптимізації

# КЛЮЧ У СЕСІЇ ДЛЯ ЗБЕРІГАННЯ ID ОБ'ЄКТА ORDER
CART_SESSION_KEY = 'order_id'


def get_or_create_cart(request):
    """
    Отримує або створює об'єкт Order (кошик) на основі ID, збереженого в сесії.
    Це забезпечує, що кошик прив'язаний до пристрою/сесії, а не до фіксованого запису "Guest".
    """

    # 1. Спробуйте отримати ID кошика з поточної сесії
    order_id = request.session.get(CART_SESSION_KEY)

    try:
        # 2. Якщо ID є, спробуйте завантажити об'єкт Order з бази даних
        if order_id:
            # pk=order_id є еквівалентом id=order_id
            order = Order.objects.get(pk=order_id, complete=False)
        else:
            # 3. Якщо ID немає (нова сесія/новий пристрій), створіть новий об'єкт
            order = Order.objects.create(complete=False, customer='Session Guest')
            # Збережіть ID нового об'єкта у сесії
            request.session[CART_SESSION_KEY] = order.pk
            request.session.modified = True

    except Order.DoesNotExist:
        # 4. Якщо об'єкт Order з цим ID був видалений з бази (або помилка), створити новий
        order = Order.objects.create(complete=False, customer='Session Guest')
        request.session[CART_SESSION_KEY] = order.pk
        request.session.modified = True

    return order


# =========================================================================
# 1. ОСНОВНІ VIEWS (ЗМІНЮВАТИ НЕ ПОТРІБНО, вони викликають нову get_or_create_cart)
# =========================================================================

def home(request):
    order = get_or_create_cart(request)
    cart_items = order.get_cart_items
    categories = Product.CATEGORY_CHOICES
    latest_products = Product.objects.all().order_by('-id')[:6]
    return render(request, 'store/home.html',
                  {'cart_items': cart_items, 'latest_products': latest_products, 'categories': categories})


def store(request):
    category_slug = request.GET.get('category')

    if category_slug:
        products = Product.objects.filter(category=category_slug)
    else:
        products = Product.objects.all()

    order = get_or_create_cart(request)
    cart_items = order.get_cart_items

    context = {
        'products': products,
        'cart_items': cart_items,
        'categories': Product.CATEGORY_CHOICES,
        'current_category': category_slug
    }
    return render(request, 'store/catalog.html', context)


# Заглушки для інших сторінок (викликають нову get_or_create_cart)
def about(request):
    order = get_or_create_cart(request)
    return render(request, 'store/about.html',
                  {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})


def blog(request):
    order = get_or_create_cart(request)
    return render(request, 'store/blog.html',
                  {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})


def contact(request):
    order = get_or_create_cart(request)
    return render(request, 'store/contact.html',
                  {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})


# =========================================================================
# 2. ФУНКЦІОНАЛЬНІ VIEWS (ЗМІНЮВАТИ НЕ ПОТРІБНО)
# =========================================================================

def cart(request):
    order = get_or_create_cart(request)
    items = order.orderitem_set.all()
    cart_total = order.get_cart_total
    cart_items = order.get_cart_items

    context = {'items': items, 'order': order, 'cart_items': cart_items, 'cart_total': cart_total}
    return render(request, 'store/cart.html', context)


def checkout(request):
    order = get_or_create_cart(request)
    items = order.orderitem_set.all()
    cart_total = order.get_cart_total
    cart_items = order.get_cart_items

    context = {'items': items, 'order': order, 'cart_items': cart_items, 'cart_total': cart_total}
    return render(request, 'store/checkout.html', context)


# ФУНКЦІЯ ОБРОБКИ AJAX
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    order = get_or_create_cart(request)
    product = Product.objects.get(id=productId)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)