from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product, Order, OrderItem


# Тимчасова функція для імітації кошика гостя
def get_or_create_cart(request):
    try:
        order = Order.objects.get(complete=False, customer='Guest')
    except Order.DoesNotExist:
        order = Order.objects.create(complete=False, customer='Guest')
    return order

def home(request):
    order = get_or_create_cart(request)
    cart_items = order.get_cart_items
    # Отримуємо всі доступні категорії для меню
    categories = Product.CATEGORY_CHOICES
    # Отримуємо 6 нових товарів для банера
    latest_products = Product.objects.all().order_by('-id')[:6]
    return render(request, 'store/home.html', {'cart_items': cart_items, 'latest_products': latest_products, 'categories': categories})

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
        'categories': Product.CATEGORY_CHOICES, # Передаємо категорії
        'current_category': category_slug # Передаємо поточну активну категорію
    }
    return render(request, 'store/catalog.html', context)


# Заглушки для інших сторінок (додаємо категорії для навігації)
def about(request):
    order = get_or_create_cart(request)
    return render(request, 'store/about.html', {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})

def blog(request):
    order = get_or_create_cart(request)
    return render(request, 'store/blog.html', {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})

def contact(request):
    order = get_or_create_cart(request)
    return render(request, 'store/contact.html', {'cart_items': order.get_cart_items, 'categories': Product.CATEGORY_CHOICES})


# Сторінка кошика
def cart(request):
    order = get_or_create_cart(request)
    items = order.orderitem_set.all()
    cart_total = order.get_cart_total
    cart_items = order.get_cart_items

    context = {'items': items, 'order': order, 'cart_items': cart_items, 'cart_total': cart_total}
    return render(request, 'store/cart.html', context)


# Сторінка оформлення
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