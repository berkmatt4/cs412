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

    def get_context_data(self):
        '''overriding to add context objects for searching and filtering
        through all of the vehicles'''
        context = super().get_context_data()

        makes = Vehicle.objects.values('make').distinct()
        makeList = []
        for make in makes:
            makeList.append(make)

        modelSet = Vehicle.objects.values('model').distinct()
        modelList = []
        for model in modelSet:
            modelList.append(model)

        years = Vehicle.objects.values('year').distinct()
        yearList = []
        for year in years:
            yearList.append(year)

        bodyTypes = Vehicle.objects.values('body_type').distinct()
        bodyList = []
        for body in bodyTypes:
            bodyList.append(body)

        engineSizes = Vehicle.objects.values('engine_size').distinct()
        engineList = []
        for engine in engineSizes:
            engineList.append(engine)

        msrps = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]

        context['msrps'] = msrps
        context['makes'] = makeList
        context['models'] = modelList
        context['years'] = yearList
        context['bodies'] = bodyList
        context['engines'] = engineList

        #ensuring that we have persistence by keeping selections
        #even if the user refreshes
        context['selected_make'] = self.request.GET.get('make', '')
        context['selected_model'] = self.request.GET.get('model', '')
        context['selected_year'] = self.request.GET.get('year', '')
        context['selected_body'] = self.request.GET.get('body', '')
        context['selected_engine'] = self.request.GET.get('engine', '')
        context['min_msrp'] = self.request.GET.get('min_msrp', '')
        context['max_msrp'] = self.request.GET.get('max_msrp', '')
        context['mpg_above'] = self.request.GET.get('mpg_above', '')


        return context

class VehicleDetailView(DetailView):
    '''view to display the info of a single vehicle'''

    template_name = 'project/vehicle_details.html'
    model = Vehicle
    context_object_name = 'vehicle'



class SalespersonListView(ListView):
    '''view to display a list of salespeople working
    at the dealership'''

    template_name = 'project/salesperson_list.html'
    model = Salesperson
    context_object_name = 'salesperson'
    paginate_by = 10        #show 10 people per page (not sure if this will ever be used)
    

