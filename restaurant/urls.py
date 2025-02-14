from django.urls import path
from django.conf import settings
from . import views

#urls.py provides navigation within the restaurant page

urlpatterns = [
    path(r'', views.main, name = "main"),
    path(r'main', views.main, name = "main"),
    path(r'order', views.order, name = "order"),
    path(r'confirmation', views.confirmation, name = "confirmation"),
]