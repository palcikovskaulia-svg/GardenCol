from django.shortcuts import render, redirect  # Додано 'redirect'
from django.http import JsonResponse
import json
# Переконайтеся, що імпортуємо ShippingAddress
from .models import Product, Order, OrderItem, ShippingAddress
from django.db.models import Sum

# КЛЮЧ У СЕСІЇ ДЛЯ ЗБЕРІГАННЯ ID ОБ'ЄКТА ORDER
CART_SESSION_KEY = 'order_id'


def get_or_create_cart(request):
    """
    Отримує або створює об'єкт Order (кошик) на основі ID, збереженого в сесії.
    Це забезпечує, що кошик прив'язаний до пристрою/сесії.
    """
    order_id = request.session.get(CART_SESSION_KEY)

    try:
        if order_id:
            order = Order.objects.get(pk=order_id, complete=False)
        else:
            order = Order.objects.create(complete=False, customer='Session Guest')
            request.session[CART_SESSION_KEY] = order.pk
            request.session.modified = True

    except Order.DoesNotExist:
        order = Order.objects.create(complete=False, customer='Session Guest')
        request.session[CART_SESSION_KEY] = order.pk
        request.session.modified = True

    return order


# =========================================================================
# 1. ОСНОВНІ VIEWS (Відображення сторінок)
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


# Заглушки для інших сторінок
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
# 2. ФУНКЦІОНАЛЬНІ VIEWS (Кошик та Оформлення)
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
    cart_items = order.get_cart_items

    # ОБРОБКА ФОРМИ ЗАМОВЛЕННЯ
    if request.method == 'POST':
        data = request.POST

        # Перевірка, щоб не обробляти порожній кошик
        if cart_items == 0:
            return redirect('store')

            # 1. Завершення замовлення (Order)
        order.complete = True
        order.save()

        # 2. Створення адреси доставки
        ShippingAddress.objects.create(
            order=order,
            # Використовуйте імена полів з вашої форми checkout.html:
            address=data['address'],
            city=data['city'],
            # state - часто не використовується в Україні, можна замінити на 'region' або залишити
            state=data.get('state', ''),
            zipcode=data['zipcode'],
        )

        # 3. Перенаправлення на сторінку підтвердження
        return redirect('checkout_success', order_id=order.id)

    # ОБРОБКА GET-ЗАПИТУ (відображення сторінки)
    items = order.orderitem_set.all()
    cart_total = order.get_cart_total

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'store/checkout.html', context)


# НОВА ФУНКЦІЯ: Сторінка підтвердження замовлення
def checkout_success(request, order_id):
    """Відображає повідомлення про успішне оформлення замовлення."""

    try:
        order = Order.objects.get(id=order_id)
        # Очищаємо сесію, щоб кошик був порожнім після завершення замовлення
        if CART_SESSION_KEY in request.session:
            del request.session[CART_SESSION_KEY]
            request.session.modified = True

    except Order.DoesNotExist:
        return redirect('home')

    context = {
        'order_id': order.id,
        'order_total': order.get_cart_total,
        'categories': Product.CATEGORY_CHOICES,
        # Очищений кошик
        'cart_items': 0
    }
    return render(request, 'store/checkout_success.html', context)


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