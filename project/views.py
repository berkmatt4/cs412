#views file containing the views for the online car dealership

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, CreateView
from .models import *

# Create your views here.

class VehicleListView(ListView):
    '''View to display a list of vehicles currently
    on the lot'''

    template_name = 'project/vehicle_list.html'
    model = Vehicle
    context_object_name = 'vehicles'
    paginate_by = 25            #show 25 cars per page


class SalespersonListView(ListView):
    '''view to display a list of salespeople working
    at the dealership'''

    template_name = 'project/salesperson_list.html'
    model = Salesperson
    context_object_name = 'salesperson'
    paginate_by = 10        #show 10 people per page (not sure if this will ever be used)
    

