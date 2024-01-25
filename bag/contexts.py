from decimal import Decimal
from django.conf import settings
from products.models import Product
from django.shortcuts import get_object_or_404


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0

    bag = request.session.get('bag', {})
    for key in bag:
        product_id = int(key)
        bag_items.append(product_id)
        product = get_object_or_404(Product, id=product_id)
        quantity = bag[key]

        total += product.price * quantity
        product_count += quantity

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = total + delivery

    context = {
        'bag_items' : bag_items,
        'total' : total,
        'product_count' : product_count,
        'delivery' : delivery,
        'free_delivery_delta' : free_delivery_delta,
        'free_delivery_threshold' : settings.FREE_DELIVERY_THRESHOLD,
        'grand_total' : grand_total,
    }

    return context
