from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm

def profiles(request):
    """
    Display the user's profile
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")

    template = 'profiles/profile.html'
    orders = profile.orders.all()

    form = UserProfileForm(instance=profile)
    context = {
        'profile_form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Display the user's order history
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'is_past_order': True,
    }
    return render(request, template, context)
