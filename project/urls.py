#urls.py holds urlpatterns for page navigation for the
#online car dealership

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.HomepageView.as_view(), name = 'home'),
    path(r'homepage', views.HomepageView.as_view(), name = 'home_page'),
    path(r'vehicles', views.VehicleListView.as_view(), name='vehicle_list'),
    path(r'salespeople', views.SalespersonListView.as_view(), name = 'salespeople'),
    path(r'vehicle_details/<int:pk>', views.VehicleDetailView.as_view(), name = 'vehicle_details'),
    path(r'customers', views.CustomerListView.as_view(), name = 'customers'),
    path(r'customer_details/<int:pk>', views.CustomerDetailView.as_view(), name='customer_details'),
    path(r'customer_details/<int:pk>/create_offer', views.CreateSalesMatchView.as_view(), name='create_offer'),
    path(r'login', auth_views.LoginView.as_view(template_name = 'project/login.html'), name='login'),
    path(r'logout', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),
    path(r'salesmatch_details/<int:pk>', views.SalesMatchDetailView.as_view(), name='salesmatch_detail'),
    path(r'salesmatches', views.SalesmatchListView.as_view(), name = 'salesmatch_list'),
    path(r'salesmatch_details/<int:pk>/update', views.UpdateSalesmatchView.as_view(), name="update_salesmatch"),
    path(r'offer_rejected', views.OfferRejectedView.as_view(), name = 'offer_rejected'),
    path(r'offer_accepted', views.OfferAcceptedView.as_view(), name = 'offer_accepted'),
    path(r'salesmatch_details/<int:pk>/decision', views.OfferDecisionView.as_view(), name = 'offer_decision'),
    path(r'vehicle_details/<int:pk>/interest', views.ExpressInterestView.as_view(), name = 'express_interest'),
    path(r'sold_vehicles', views.SoldVehicleListView.as_view(), name="sold_vehicles"),
    path(r'wrong_passkey', views.InvalidPasskeyView.as_view(), name='invalid_passkey'),
    path(r'register/customer', views.CreateCustomerView.as_view(), name = 'register_customer'),
    path(r'register/salesperson', views.CreateSalespersonView.as_view(), name = 'register_salesperson'),
    path(r'delete_account', views.DeleteAccountView.as_view(), name = 'delete_account'),
    path(r'add_vehicle', views.CreateVehicleView.as_view(), name="add_vehicle"),
    path(r'salesperson_details/<int:pk>/review', views.CreateSalespersonReview.as_view(), name = "salesperson_review"),
    path(r'salesperson_details/<int:pk>', views.SalespersonDetailView.as_view(), name = "salesperson_details"),
    path(r'salesperson_details/<int:pk>/update', views.UpdateSalesReview.as_view(), name = 'update_sales_review'),
    path(r'salesperson_details/<int:pk>/delete', views.DeleteSalesReview.as_view(), name = 'delete_sales_review'),
    

]