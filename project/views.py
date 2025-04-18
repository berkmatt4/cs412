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

    def get_queryset(self):
        '''function which allows us to filter and search'''
        vehicles = super().get_queryset()

        if 'make' in self.request.GET:
            make = self.request.GET['make']
            if make:
                vehicles = vehicles.filter(make = make)

        if 'model' in self.request.GET:
            model = self.request.GET['model']
            if model:
                vehicles = vehicles.filter(model = model)
        
        if 'year' in self.request.GET:
            year = self.request.GET['year']
            if year:
                vehicles = vehicles.filter(year = year)

        if 'body' in self.request.GET:
            body = self.request.GET['body']
            if body:
                vehicles = vehicles.filter(body_type = body)

        if 'engine' in self.request.GET:
            engine = self.request.GET['engine']
            if engine:
                vehicles = vehicles.filter(engine_size = engine)

        if 'max_msrp' in self.request.GET:
            max_msrp = self.request.GET['max_msrp']
            if max_msrp:
                vehicles = vehicles.filter(msrp__lte = max_msrp)

        if 'min_mpg' in self.request.GET:
            min_mpg = self.request.GET['min_mpg']
            if min_mpg:
                vehicles = vehicles.filter(mpg__gte = min_mpg)

        return vehicles

    def get_context_data(self):
        '''overriding to add context objects for searching and filtering
        through all of the vehicles'''
        context = super().get_context_data()

        makes = Vehicle.objects.values('make').distinct()
        makeList = []
        for make in makes:
            makeList.append(make['make'])
        makeList.sort()
        

        modelSet = Vehicle.objects.values('model').distinct()
        modelList = []
        for model in modelSet:
            modelList.append(model['model'])
        modelList.sort()

        years = Vehicle.objects.values('year').distinct()
        yearList = []
        for year in years:
            yearList.append(year['year'])
        yearList.sort()

        bodyTypes = Vehicle.objects.values('body_type').distinct()
        bodyList = []
        for body in bodyTypes:
            bodyList.append(body['body_type'])
        bodyList.sort()

        engineSizes = Vehicle.objects.values('engine_size').distinct()
        engineList = []
        for engine in engineSizes:
            engineList.append(engine['engine_size'])
        engineList.sort()

        msrpSet = Vehicle.objects.values('msrp').distinct()
        msrpList = []
        for msrp in msrpSet:
            msrpList.append(msrp['msrp'])

        min_msrp = min(msrpList)
        max_msrp = max(msrpList)
        increment = 10000

        start_value = ((min_msrp // increment) + 1) * increment
        end_value = ((max_msrp // increment) + 1) * increment

        msrps = list(range(start_value, end_value + increment, increment))
        msrps.sort()

        mpgSet = Vehicle.objects.values('mpg').distinct()
        mpgList = []
        for mpg in mpgSet:
            mpgList.append(mpg['mpg'])
        
        min_mpg = min(mpgList)
        max_mpg = max(mpgList)
        increment = 5

        start_value = ((min_mpg // increment) + 1) * increment
        end_value = ((max_mpg // increment) +  1) * increment

        mpgs = list(range(start_value - increment, end_value, increment))
        mpgs.sort()

        context['mpgs'] = mpgs
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
        context['max_msrp'] = self.request.GET.get('max_msrp', '')
        context['min_mpg'] = self.request.GET.get('min_mpg', '')


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

class CustomerListView(ListView):
    '''view to display active customers shopping at the 
    dealership'''

    template_name = 'project/customer_list.html'
    model = Customer
    context_object_name = 'customer'
    paginate_by = 10            #show 10 people per page


    

