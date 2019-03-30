from django import template

register = template.Library()


@register.filter(name='yellow_stars')
def yellow_stars(number):
    return range(number)


@register.filter(name='gray_stars')
def gray_stars(number):
    return range(5-number)


@register.filter
def calculate_price(obj, days):
    return round(obj.monthly_cost / 30 * days)


@register.filter
def get_first_image_url(images):
    images = list(images)
    if len(images):
        return list(images)[0].image.url
    else:
        return "Unknown"

@register.simple_tag
def is_user(user, email):
    return user.email.lower() != email.lower()
