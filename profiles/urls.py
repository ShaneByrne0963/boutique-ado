from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='view_profile'),
]
