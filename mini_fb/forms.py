from django import forms
from .models import Profile, StatusMessage

#forms.py provides the forms for the user to enter a new profile
#or to enter new status  messages

class CreateProfileForm(forms.ModelForm):
    '''A form with which users can create
    a new profile'''

    class Meta:
        '''class to associate the form with a model in our db'''
        model = Profile

        #outlining which fields should be filled by the user
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form with which users can create a new status 
    message'''

    class Meta:
        '''class to associate the form with a model in the db'''
        model = StatusMessage

        #only field needed here is message
        fields = ['message']