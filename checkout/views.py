from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Oead4LrGvNYuhY8Ex36ERmeNJA8RI6jClXcYGEiBvrx4vJtlHlvXkUma2V9c3y4kCioB1NHYVmsTaKNIMEa7WPH00VtJTP1YG',
        'client_secret': 'test',
    }

    return render(request, template, context)
