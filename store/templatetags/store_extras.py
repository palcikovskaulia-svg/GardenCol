from django import template
from ..models import Product  # Відносний імпорт

register = template.Library()

@register.filter
def get_category_name(categories, slug):
    """
    Повертає повну назву категорії за slug.
    Використання: {{ categories|get_category_name:current_category }}
    """
    if not categories or not slug:
        return "Усі товари"

    for cat_slug, cat_name in categories:
        if cat_slug == slug:
            return cat_name

    return "Невідома категорія"