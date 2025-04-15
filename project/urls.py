#urls.py holds urlpatterns for page navigation for the
#online car dealership

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VehicleListView.as_view(), name = 'home'),
    path(r'vehicles', views.VehicleListView.as_view(), name='vehicle_list'),
    path(r'salespeople', views.SalespersonListView.as_view(), name = 'salespeople'),
    
]