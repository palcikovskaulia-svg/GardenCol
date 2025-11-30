from django import template
from store.models import Product # Можливо, цей імпорт не потрібен, якщо категорія береться з контексту

register = template.Library()

@register.filter
def get_category_name(choices_list, key):
    """
    Повертає повну назву категорії за її коротким кодом (slug).
    Використання: {{ categories|get_category_name:current_category }}
    """
    # choices_list - це Product.CATEGORY_CHOICES, який є списком кортежів
    if not choices_list or not key:
        return "Усі товари"

    for slug, name in choices_list:
        if slug == key:
            return name
    return "Невідома категорія"