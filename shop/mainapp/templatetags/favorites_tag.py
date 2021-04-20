from django import template
from django.contrib.auth.models import User

from mainapp.models import Customer


register = template.Library()


@register.simple_tag()
def get_favorites_count(user):
    customer = Customer.objects.get(user=user)
    return customer.favorite_set.all().count()


@register.simple_tag()
def check_favorites(user):
    print(1)
    customer = Customer.objects.get(user=user)
    print(customer.favorites.get_queryset())
    