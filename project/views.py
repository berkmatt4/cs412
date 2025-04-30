#views file containing the views for the online car dealership

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''A custom mixin which verifies if a user is a customer or not'''

    def test_func(self):
        '''testing if the user is a customer'''
        return Customer.objects.filter(user=self.request.user).exists()
    
    def handle_no_permission(self):
        '''gracefully handling if a user is not a customer (doesn't have the right permissions)'''
        if self.request.user.is_authenticated:
            raise PermissionDenied("You must be a customer to access this page")
        return super().handle_no_permission()
    
class SalespersonRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''custom mixin which verifies if a user is a salesperson or not'''

    def test_func(self):
        '''testing if the user is a salesperson'''
        return Salesperson.objects.filter(user=self.request.user).exists()
    
    def handle_no_permission(self):
        '''gracefully handling if a user is not a salesperson and has no access'''
        if self.request.user.is_authenticated:
            raise PermissionDenied("You must be a salesperson to access this page")
        return super().handle_no_permission()



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

        vehicles = vehicles.filter(isSold = False)

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

class CustomerListView(SalespersonRequiredMixin, ListView):
    '''view to display active customers shopping at the 
    dealership. also allows salespeople to filter by those interested
    in a vehicle so they can offer a price
    only salespeople can see this list for privacy, of course '''

    template_name = 'project/customer_list.html'
    model = Customer
    context_object_name = 'customer'
    paginate_by = 10            #show 10 people per page

    def get_queryset(self):
        '''function to filter by customers interested
        in a vehicle'''
        customer = super().get_queryset()

        if 'show_interested' in self.request.GET:
            customer = customer.filter(interested_in__isnull = False)

            existing_matches = SalesMatch.objects.values('customer').distinct()
            customer = customer.exclude(id__in=existing_matches)

        return customer
    
    def get_context_data(self):
        '''overriding to provide persistence in filtering customers'''
        context = super().get_context_data()

        context['show_interested_checked'] = self.request.GET.get('show_interested', '')

        return context
    
class CustomerDetailView(DetailView):
    '''A view to show a customer's details which salespeople can
    use to create salesmatches
    only salespeople can see this page, for privacy, of course!'''

    template_name = 'project/customer_detail.html'
    model = Customer
    context_object_name = 'customer'

class CreateSalesMatchView(SalespersonRequiredMixin, CreateView):
    '''A view which allows only salespeople to assign themselves to help
    customers and offer a price for the vehicle'''

    template_name = 'project/create_salesmatch.html'
    model = SalesMatch
    form_class = CreateSalesmatchForm
    
    def get_context_data(self, **kwargs):
        '''getting the customer and assigning it to a context variable'''
        context = super().get_context_data()
 
        customer = Customer.objects.get(id = self.kwargs.get('pk'))
        context['customer'] = customer

        return context

    def form_valid(self, form):
        '''overriding to create the salesmatch object using the given
        information plus the inputted information'''

        form.instance.customer = Customer.objects.get(id = self.kwargs.get('pk'))
        form.instance.salesperson = Salesperson.objects.get(user=self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        '''redirecting to the salesmatch created'''
        return reverse('salesmatch_list')
    
class SalesMatchDetailView(LoginRequiredMixin, DetailView):
    '''A view to show a created salesmatch. Will only be accessible to
    the customer and salesperson involved in the sale'''

    template_name = 'project/salesmatch_detail.html'
    model = SalesMatch
    context_object_name = 'salesmatch'

    def get_object(self):

        salesmatch = SalesMatch.objects.get(pk = self.kwargs['pk'])

        user = self.request.user

        customer = salesmatch.customer
        salesperson = salesmatch.salesperson

        try:
            customer = Customer.objects.get(user=user)
            if salesmatch.customer.pk == customer.pk:
                return salesmatch
        except Customer.DoesNotExist:
            pass

        try:
            salesperson = Salesperson.objects.get(user=user)
            if salesperson:
                return salesmatch
        except Salesperson.DoesNotExist:
            pass

        raise PermissionDenied("you are not authorized to view this salesmatch")
        
    def get_context_data(self, **kwargs):
        '''overriding to attach some more pricing info to the vehicle'''
        context = super().get_context_data(**kwargs)

        tax_rate = 1.05

        match = SalesMatch.objects.get(pk = self.kwargs['pk'])

        credit_score = match.customer.credit_score

        interest_rate = 0

        if credit_score >= 750:
            interest_rate_calc = 1.039
            interest_rate = 3.9
        elif credit_score >=650 and credit_score < 750:
            interest_rate_calc = 1.049
            interest_rate = 4.9
        else:
            interest_rate_calc = 1.059
            interest_rate = 5.9

        other_fees = 750

        context['tax'] = tax_rate
        context['interest'] = interest_rate
        context['fees'] = other_fees

        total_price = (match.price * tax_rate) + other_fees
        context['total_price'] = round(total_price, 2)

        first_payment = (total_price * interest_rate_calc) / 60

        context['first_payment'] = round(first_payment, 2)
        context['salesmatch'] = match

        return context

class SalesmatchListView(LoginRequiredMixin, ListView):
    '''a view to display the list of salesmatches
    If the user is a salesperson, they can see all of them
    if the user is a customer, they can only see the one that applies to them'''

    template_name = 'project/salesmatch_list.html'
    model = SalesMatch
    context_object_name = "salesmatches"

    def get_queryset(self):
        '''filtering salesmatches by the user role'''

        queryset = super().get_queryset()

        customer = Customer.objects.filter(user = self.request.user).first()
        if customer:

            return queryset.filter(customer=customer)
        
        salesperson = Salesperson.objects.filter(user = self.request.user).first()
        if salesperson:
            return queryset

class UpdateSalesmatchView(SalespersonRequiredMixin, UpdateView):
    '''A view where salespeople can update a salesmatch'''
    model = SalesMatch
    form_class = UpdateSalesmatchForm
    template_name = 'project/update_salesmatch_form.html'

    def get_success_url(self):
        '''overriding to display salesmatch after update'''

        pk = self.kwargs['pk']

        salesmatch = SalesMatch.objects.get(pk=pk)

        return reverse('salesmatch_detail', kwargs={'pk':pk})
    
class OfferDecisionView(CustomerRequiredMixin, UpdateView):
    '''a view for the customer to either accept or reject a sales offer.
    In both cases, the SalesMatch will be deleted'''

    model = SalesMatch
    form_class = OfferDecisionForm
    template_name = 'project/offer_decision_form.html'
    context_object_name = 's'

    def get_object(self):
        '''ensuring that the only person making the decision is
        the relevant customer'''

        pk = self.kwargs.get('pk')
        salesmatch = SalesMatch.objects.get(pk=pk)

        user = self.request.user
        try:
            customer = Customer.objects.get(user=user)

            if salesmatch.customer.pk == customer.pk:
                return salesmatch
        except:
            pass
        
        raise PermissionDenied("You are not authorized to make a decision on this offer")
    
    def form_valid(self, form):
        '''process form submission ensuring we delete the salesmatch if rejected, and 
        if accepted delete salesmatch and mark vehicle as sold'''

        decision = form.cleaned_data
        choice = decision.get('decision')

        if choice == 'accept':
            vehicle = self.object.customer.interested_in

            vehicle.isSold = True
            vehicle.save()

            Customer.objects.filter(interested_in = vehicle).update(interested_in = None)
            self.object.delete()

            return HttpResponseRedirect(reverse('offer_accepted'))

        else:
            vehicle = self.object.customer.interested_in

            Customer.objects.filter(interested_in = vehicle).update(interested_in = None)
            self.object.delete()
            return HttpResponseRedirect(reverse('offer_rejected'))

class OfferAcceptedView(TemplateView):
    '''a view that will be displayed if a customer accepts their sales offer'''

    template_name = 'project/offer_accepted.html'
    model = Customer

class OfferRejectedView(TemplateView):
    '''a view that will be displayed if a customer rejects their sales offer'''

    template_name  = 'project/offer_rejected.html'
    model = Customer

class ExpressInterestView(CustomerRequiredMixin, DetailView):
    '''view to handle customers expressing interest in a vehicle'''
    model = Vehicle
    template_name = 'project/express_interest.html'
    context_object_name = 'v'

    def post(self, request, *args, **kwargs):
        '''handle the post request when declaring interested'''

        vehicle = self.get_object()

        customer = Customer.objects.get(user=request.user)

        customer.interested_in=vehicle
        customer.save()

        return self.get(request, *args, **kwargs)


class SoldVehicleListView(SalespersonRequiredMixin, ListView):
    '''a view to show all vehicles that have been sold'''

    model = Vehicle
    template_name = 'project/vehicles_sold.html'
    context_object_name = 'vehicles'
    paginate_by = 25

    def get_queryset(self):
        '''overriding to only get sold vehicles'''

        vehicles = Vehicle.objects.all()

        vehicles = vehicles.filter(isSold=True)
        return vehicles
    
class CreateCustomerView(CreateView):
    '''a view to allow users to register as customers'''
    form_class = CreateCustomerForm
    template_name = 'project/customer_registration.html'

    def get_context_data(self):
        '''adding the usercreationform as context data (provided by django)'''

        context = super().get_context_data()
        

        context['user_creation_form'] = UserCreationForm

        return context
    
    def form_valid(self, form):
        '''creating a new User object and attach it to the newly created
        customer object'''

        user = UserCreationForm(self.request.POST)

        savedUser = user.save()

        form.instance.user = savedUser

        login(self.request, savedUser)

        return super().form_valid(form)
    
class CreateSalespersonView(CreateView):
    '''a view to allow users to register as salespeople
    requires a secret passkey so not just anyone can do it'''

    form_class = CreateSalespersonForm
    template_name = 'project/salesperson_registration.html'

    def get_context_data(self):
        '''adding the usercreationform to the context data'''

        context = super().get_context_data()

        context['user_creation_form'] = UserCreationForm

        return context
    
    def form_valid(self, form):
        '''creating the user object and attaching it to the new salesperson
        also validating the passkey'''

        passkey = form.cleaned_data.get('passkey')
        if passkey != "dealershipStaff":
            return self.form_invalid(form)
        
        user = UserCreationForm(self.request.POST)

        savedUser = user.save()

        form.instance.user = savedUser

        login(self.request, savedUser)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('invalid_passkey'))

class InvalidPasskeyView(TemplateView):
    '''a view for when a user attempts to register as a salesperson
    but provides an invalid passkey'''

    template_name = 'project/wrong_passkey.html'

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    '''A view to allow any user to delete their account'''

    model = User
    template_name = 'project/delete_account.html'
    
    def get_object(self):
        '''return users account'''
        return self.request.user
    
    def get_success_url(self):
        '''overriding to return to the home page after
        successfully deleting a user from the dealership'''


        return reverse('home')
    
class CreateVehicleView(SalespersonRequiredMixin, CreateView):
    '''A view to allow salespeople to add vehicles to the lot'''

    form_class = CreateVehicleForm
    template_name = 'project/create_vehicle.html'

    def get_success_url(self):
        '''redirect to the newly created vehicle'''
        return reverse('vehicle_details', kwargs = {'pk': self.object.pk})
    
    def form_valid(self, form):
        '''set isSold to false before creating the vehicle'''
        form.instance.isSold = False
        return super().form_valid(form)
    
class CreateSalespersonReview(CustomerRequiredMixin, CreateView):
    '''A view to allow customers to create reviews for salespeople'''

    model = SalespersonReview
    form_class = CreateSalespersonReviewForm
    template_name = 'project/create_sales_review.html'

    def get_context_data(self, **kwargs):
        '''grabbing the salesperson from the context data'''

        context =  super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')

        salesperson = Salesperson.objects.get(pk=pk)
        context['salesperson'] = salesperson
        return context
    
    def form_valid(self, form):
        '''setting the customer and salesperson for the review'''

        form.instance.customer = Customer.objects.get(user=self.request.user)
        form.instance.salesperson = Salesperson.objects.get(pk=self.kwargs.get('pk'))

        return super().form_valid(form)
    
    def get_success_url(self):
        '''redirect the user to the salesperson detail page'''

        return reverse('salesperson_details', kwargs={'pk': self.kwargs.get('pk')})
    
class SalespersonDetailView(DetailView):
    '''a class showing the details of a single salesperson
    also displays user reviews about that salesperson'''

    model = Salesperson
    template_name = 'project/salesperson_detail.html'
    context_object_name = 's'

class UpdateSalesReview(CustomerRequiredMixin, UpdateView):
    '''a view allowing users to update their reviews of salespeople'''

    model = SalespersonReview
    template_name = 'project/update_sales_review.html'
    form_class = UpdateSalesReviewForm
    context_object_name = 'review'

    def get_success_url(self):
        '''display salespersons detail page after deletion'''

        pk = self.kwargs['pk']
        review = SalespersonReview.objects.get(pk=pk)

        salesperson = review.salesperson
        return reverse('salesperson_details', kwargs={'pk': salesperson.pk})
    
class DeleteSalesReview(CustomerRequiredMixin, DeleteView):
    '''a view which allows users to delete their reviews'''

    model = SalespersonReview
    template_name = 'project/delete_sales_review.html'
    context_object_name = 'r'

    def get_success_url(self):
        '''After deleting the review, display the salespersons details'''

        pk = self.kwargs['pk']
        review = SalespersonReview.objects.get(pk=pk)

        salesperson = review.salesperson
        return reverse('salesperson_details', kwargs = {'pk': salesperson.pk})

