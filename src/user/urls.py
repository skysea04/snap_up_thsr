from django.urls import path

from . import views

urlpatterns = [
    path('', views.register_page, name='register_page'),
]
