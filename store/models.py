from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User



# =================================================================
# 1. МОДЕЛІ МАГАЗИНУ ТА ПРОДУКЦІЇ
# =================================================================

class Product(models.Model):
    # Категорії
    CATEGORY_CHOICES = [
        ('conifers', 'Хвойні рослини'),
        ('fruit_trees', 'Плодові дерева та кущі'),
        ('grass_seeds', 'Насіння трави'),
        ('indoor', 'Кімнатні рослини'),
        ('tools', 'Інструменти та Добрива'),
    ]

    name = models.CharField(max_length=200, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    # Зображення обробляється Cloudinary
    image = CloudinaryField('image', null=True, blank=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='indoor')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        # Повертає URL від Cloudinary
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''


class Order(models.Model):
    # Customer: Зберігаємо загальну інформацію про клієнта/сесію.
    # Може бути перетворено на ForeignKey до User, якщо додамо реєстрацію.
    customer = models.CharField(max_length=200, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)  # True, якщо замовлення оформлено
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


# =================================================================
# 2. МОДЕЛЬ АДРЕСИ ДОСТАВКИ (КРИТИЧНО ДЛЯ CHECKOUT)
# =================================================================

class ShippingAddress(models.Model):
    # Прив'язуємо до замовлення. ForeignKey, бо одне замовлення має одну адресу.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address