from django import template
from django.contrib.auth import get_user_model
from django.db.models import Sum

from chipi.models import *


register = template.Library()

@register.simple_tag
def get_cart(filter=None):
    # u = get_user_model()


    if not filter:
        return 0
    else:
        buyer = Buyer.objects.get(user_id=filter)
        return Cart.objects.filter(user=buyer).aggregate(total_count=Sum('count'))['total_count'] or 0
        # return Cart.objects.filter(user=buyer).count()
    return 0


@register.simple_tag
def get_category():
    cat = ProdCategory.objects.all()
    return cat
