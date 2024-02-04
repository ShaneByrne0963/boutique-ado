from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='view_profile'),
    path('order/<order_number>', views.order_history, name='order_history')
]
