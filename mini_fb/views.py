#views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
import random
from django.urls import reverse

# Create your views here.
class ShowAllProfilesView(ListView):
    '''defining a view to show all profiles'''

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''view to show a single profile'''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    '''a view to allow users to create a profile
    based off of the form outlined in forms.py'''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    '''a view to allow users to upload a new status
    message based on the form outlined in forms.py'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''overriding this method to direct us back
        to the profile to which the status message was uploaded'''

        pk = self.kwargs['pk']

        return reverse('show_profile', kwargs = {'pk': pk}) #need to get reverse URL to display the profile associated with the status message
    
    def get_context_data(self):
        '''overriding this method in order to retrieve
        the profile associated with the status message'''

        #using the superclass method to get the profile associated with the status message
        #this allows us to display data relating to the profile on the page
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk = pk)

        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        '''validate our data before it is sent to the db'''

        print(form.cleaned_data)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)    #must make sure that our data is associated with a PK

        form.instance.profile = profile

        return super().form_valid(form)