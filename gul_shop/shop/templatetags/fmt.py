from django import template

register = template.Library()


@register.filter
def som(value):
    """12900 -> '12 900'"""
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return value
