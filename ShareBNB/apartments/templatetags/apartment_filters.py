from django import template

register = template.Library()


@register.filter(name='yellow_stars')
def yellow_stars(number):
    return range(number)


@register.filter(name='gray_stars')
def gray_stars(number):
    return range(5-number)
