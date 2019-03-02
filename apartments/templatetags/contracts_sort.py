from django import template
register = template.Library()

@register.filter
def sort_contracts(queryset):
    return queryset.order_by('pending', 'start_date')