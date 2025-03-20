#views for the mini_fb app
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView, View
from .models import *
from .forms import *
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

        sm = form.save()    #save the form data
        files = self.request.FILES.getlist('files') #grabbing all files from the form
        print("Submitted files: ", files)

         #now we need to save the files as images    
        for file in files:

            #create the image object using submitted file and the profile
            image = Image()
            image.image_file = file
            image.profile = profile
            image.save()
            print("Printing image: ", image)

            #create the status_image object using the image object and sm object (status message)
            status_image = StatusImage()
            status_image.image_file = image
            status_image.status_message = sm
            status_image.save()
            print("Printing status image: ", status_image)


        return super().form_valid(form)
    
class UpdateProfileView(UpdateView):
    '''Class which provides a view to use the UpdateProfileForm'''

    model = Profile     #specify the model to update
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    '''a view used to delete status messages'''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self):
        '''overriding this method to display the profile
        after deleting the status message'''
        print("Before everything")
        #find pk of status message
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk) #lookup sm by pk
        print("status ", status_message)
        #find the pk of the profile and use it to reverse back to it
        profile = status_message.profile
        print("Profile", profile)
        return reverse('show_profile', kwargs = {'pk': profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''a class used to update status messages'''

    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    form_class = UpdateStatusForm
    context_object_name = "status_message"

    def get_success_url(self):
        '''overriding to display profile page'''

        #find pk of status
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)

        #get pk of profile
        profile = status_message.profile

        return reverse('show_profile', kwargs = {'pk': profile.pk})
    
class AddFriendView(View):
    '''a generic view which allows the user to add a friend'''

    def dispatch(self, request, *args, **kwargs):
        '''method which will associate two profiles into 
        the Friend relationship'''

        #overriding this method to grab the kwargs of the url
        pk = self.kwargs['pk']
        otherPk = self.kwargs['other_pk']

        #use those values to fetch both profiles, then call add_friend
        profile1 = Profile.objects.get(pk=pk)
        profile2 = Profile.objects.get(pk=otherPk)

        profile1.add_friend(profile2)

        #had trouble with using reverse, so I used redirect instead to get back to the original profile
        return redirect('show_profile', pk = pk)
    
class ShowFriendSuggestionsView(DetailView):
    '''A view to show suggestions for friends of a given profile'''

    template_name = "mini_fb/friend_suggestions.html"
    model = Profile


class ShowNewsFeedView(DetailView):
    '''a view to show the news feed for a given profile
    shows status messages, images'''

    template_name = "mini_fb/news_feed.html"
    model = Profile