from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """
    A view to show individual product details
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # Search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            q = Q(Q(name__icontains=query) | Q(description__icontains=query))
            products = products.filter(q)

        # Categories
        if 'category' in request.GET:
            category = request.GET['category']
            if not category:
                messages.error(request, "No categories entered. Please try again")
                return redirect(reverse('products'))
            categories = category.split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products' : products,
        'search_term' : query,
        'current_categories' : categories,
        'current_sorting' : current_sorting
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show all products, including sorting and search queries
    """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product' : product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Add a product to the store
    """

    # Prevents non-administrators from adding products
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform that action.')
        return redirect(reverse('home'))

    form = None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'product_form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit a product
    """

    # Prevents non-administrators from editing products
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform that action.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    form = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    
    template = 'products/edit_product.html'
    context = {
        'product_form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Deletes a product from the database
    """

    # Prevents non-administrators from deleting products
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform that action.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Successfully deleted product!')
    return redirect(reverse('products'))
