#defines data models for the blog app

from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulate the data of a blog article'''

    #data attributes
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published=models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''return a string representation of a model instance'''

        return f'{self.title} by {self.author}'