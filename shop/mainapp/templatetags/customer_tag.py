from django import template
from django.contrib.auth.models import User

from mainapp.models import Customer


register = template.Library()

@register.simple_tag()
def get_customer(user):
    return Customer.objects.get(user=user)


@register.simple_tag()
def get_cartproduct_count(user):
    customer = Customer.objects.get(user=user)
    cart = customer.cart_set.get(status=1)
    return cart.cartproduct_set.all().count()
    