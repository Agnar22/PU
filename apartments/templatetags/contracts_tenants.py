from django import template
import datetime

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

@register.simple_tag
def is_finished(obj):
    return obj.end_date < datetime.datetime.today().date()
