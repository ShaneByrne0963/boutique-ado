from django.shortcuts import render, redirect, reverse, HttpResponse, \
                             get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """
    A view to render the bag contents page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    A view to add an item to the bag
    """
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST.get('product_size')
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = { 'items_by_size' : { size : quantity } }
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified item to the specified amount
    """
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST.get('product_size')
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
    
    request.session['bag'] = bag
    return redirect(reverse('bag'))


def remove_item(request, item_id):
    """
    Remove the specified item from the shopping bag
    """
    try:
        product = get_object_or_404(Product, id=item_id)
        bag = request.session.get('bag', {})
        size = None
        if 'product_size' in request.POST:
            size = request.POST.get('product_size')

        if size:
            del bag[item_id]['items_by_size'][size]
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
        
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.danger(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
