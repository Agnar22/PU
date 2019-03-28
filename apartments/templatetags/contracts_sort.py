from django import template
from django.db.models import Q
register = template.Library()




@register.filter
def sort_contracts(queryset):
    return queryset.order_by('pending', '-owner_approved', 'start_date')


@register.filter
def sort_contracts_owner(queryset):
    return queryset.order_by('-owner_approved', 'start_date')


@register.simple_tag
def filter_contracts(contract, email):
    print(email)
    print(contract.tenant.email)

    if contract.tenant.email.lower() == email.lower() or email.lower() in (c.lower() for c in contract.tenants):
        return True
    return False


