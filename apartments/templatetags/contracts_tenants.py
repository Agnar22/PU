from django import template
register = template.Library()

@register.filter
def calculate_tenant_amount(obj):
    return len(obj.tenants)

@register.simple_tag
def is_co_rented_by_group(obj):
    return len(obj.tenants) > 1

@register.simple_tag
def is_co_rented_by_single(obj):
    return len(obj.tenants) == 1
