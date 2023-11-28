from django.urls import path

from . import views

urlpatterns = [
    path('choices', views.booking_request_choices, name='booking_request_choices'),
    path('create', views.create_booking_request, name='create_booking_request'),
]
