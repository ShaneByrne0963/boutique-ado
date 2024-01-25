from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """
    A view to show individual product details
    """
    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            q = Q(Q(name__icontains=query) | Q(description__icontains=query))
            products = products.filter(q)
        elif 'category' in request.GET:
            category = request.GET['category']
            if not category:
                messages.error(request, "No categories entered. Please try again")
                return redirect(reverse('products'))
            categories = category.split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    context = {
        'products' : products,
        'search_term' : query,
        'current_categories': categories
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
