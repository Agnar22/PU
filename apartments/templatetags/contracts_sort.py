from django import template
register = template.Library()

@register.filter
def sort_contracts(queryset):
    return queryset.order_by('pending', '-owner_approved', 'start_date')


@register.filter
def sort_contracts_owner(queryset):
    return queryset.order_by('-owner_approved', 'start_date')
