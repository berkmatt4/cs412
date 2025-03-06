#models for the mini_fb assignment

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''model for profiles on our mini_fb app
    text fields for f_name, l_name, city, and email
    url field for the image'''
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank = True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''return a string representation of the user's profile'''
        return f'{self.first_name} {self.last_name}'

    def get_status_message(self):
        '''accessor to return the status messages related to the profile'''
        status = StatusMessage.objects.filter(profile = self)

        #sorting status messages with most recent displayed first
        sorted_status = status.order_by('-published')

        return sorted_status
    
    def get_absolute_url(self):
        '''method to show the new record after creation'''

        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    '''model for creating status messages on our mini facebook
    includes a foreign key reference for the users Profile'''
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    message = models.TextField(blank = False)
    published = models.DateTimeField(auto_now = True)   #get the current time

    def __str__(self):
        '''create a string representation of a StatusMessage object'''
        return f'{self.message}'
    
    def get_images(self):
        '''function to retrieve all images associated with the model'''
        #getting all status images associated with this status message
        status_images = StatusImage.objects.filter(status_message = self)
        images = []
        for img in status_images:
            images.append(img.image_file)
        return images



class Image(models.Model):
    '''A model to store images as files
    Includes a foreign key to the Profile attached to the image'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  #foreign key reference for a profile
    image_file = models.ImageField(blank = False)
    timestamp = models.DateTimeField(auto_now = True)
    caption = models.TextField(blank=True)  #making this field optional

    def __str__(self):
        '''defining a toString method to print the image'''
        return f'{self.profile.first_name} image: {self.image_file}'
    
class StatusImage(models.Model):
    '''Representation of an image corresponding to a status message
    includes two foreign keys: image_file, and status_message'''

    image_file = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
