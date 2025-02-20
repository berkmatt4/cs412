#models for the mini_fb assignment

from django.db import models

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