#views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random

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