# from django.contrib import admin
# from .models import Product, Order, OrderItem
#
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, ShippingAddress  # Переконайтеся, що імпортуємо всі моделі


# -----------------
# 1. КОНТЕЙНЕРИ INLINE (Відображають деталі в середині сторінки Order)
# -----------------

# 1.1. Відображення товарів у замовленні (OrderItem)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # Поля, які будуть відображатися
    fields = ['product', 'quantity', 'get_total']
    # Робимо їх лише для читання
    readonly_fields = ['product', 'quantity', 'get_total']
    extra = 0  # Не відображати порожні рядки
    can_delete = False  # Заборонити видалення товарів із завершеного замовлення

    # Додаємо метод для красивого відображення загальної суми товару
    def get_total(self, obj):
        return f"{obj.get_total:.2f} ₴"

    get_total.short_description = "Сума товару"


# 1.2. Відображення адреси доставки (ShippingAddress)
class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    # Поля адреси для зручного перегляду
    fields = ['address', 'city', 'state', 'zipcode']
    readonly_fields = ['address', 'city', 'state', 'zipcode']
    extra = 0
    max_num = 1  # Дозволено лише 1 адресу на 1 замовлення
    can_delete = False


# -----------------
# 2. НАЛАШТУВАННЯ МОДЕЛЕЙ
# -----------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 2.1. Відображення в списку (Order List View)
    list_display = (
        'id',
        'customer',
        'date_ordered',
        'display_status',  # Новий метод для красивого статусу
        'get_cart_items',
        'get_cart_total',
    )
    list_filter = ('complete', 'date_ordered')  # Фільтри збоку
    search_fields = ('id', 'customer')  # Пошук за ID та клієнтом

    # 2.2. Поля, що відображаються на сторінці деталізації
    fieldsets = (
        (None, {
            'fields': ('customer', 'date_ordered', 'transaction_id'),
        }),
        ('Статус та Сума', {
            'fields': ('complete', 'get_cart_total'),
        }),
    )

    # 2.3. Додаємо Inlines (деталізацію замовлення та адреси)
    inlines = [OrderItemInline, ShippingAddressInline]

    # 2.4. Поля лише для читання
    readonly_fields = ('date_ordered', 'get_cart_total', 'get_cart_items')

    # Метод для красивого відображення статусу (ЗЕЛЕНИЙ/ЧЕРВОНИЙ)
    def display_status(self, obj):
        if obj.complete:
            return format_html('<span style="color: green; font-weight: bold;">ЗАВЕРШЕНО</span>')
        return format_html('<span style="color: orange; font-weight: bold;">У КОШИКУ</span>')

    display_status.short_description = 'Статус'


# -----------------
# 3. РЕЄСТРАЦІЯ ІНШИХ МОДЕЛЕЙ
# -----------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Додамо фото у список товарів (якщо Cloudinary налаштовано)
    list_display = ('name', 'price', 'category', 'thumbnail')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def thumbnail(self, obj):
        if obj.image:
            # Використовуємо функцію resize від Cloudinary для прев'ю в адмінці
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.image.url)
        return ""

    thumbnail.short_description = 'Прев\'ю'

# ShippingAddress не реєструємо окремо, бо воно inlined у Order
# admin.site.register(ShippingAddress)
# admin.site.register(OrderItem) # Не реєструємо, бо воно inlined