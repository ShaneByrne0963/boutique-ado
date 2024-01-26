from decimal import Decimal
from django.conf import settings
from products.models import Product
from django.shortcuts import get_object_or_404


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item, item_data in bag.items():
        item_id = int(item)
        product = get_object_or_404(Product, id=item_id)

        if isinstance(item_data, int):
            total += product.price * item_data
            product_count += item_data
            bag_items.append({
                'item_id' : item_id,
                'quantity' : item_data,
                'product' : product,
            })
        else:
            for size, quantity in item_data['items_by_size'].items():
                total += product.price * quantity
                product_count += quantity
                bag_items.append({
                    'item_id' : item_id,
                    'quantity' : quantity,
                    'product' : product,
                    'size' : size
                })

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
