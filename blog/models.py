#defines data models for the blog app

from django.db import models
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    '''Encapsulate the data of a blog article'''

    #data attributes
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published=models.DateTimeField(auto_now=True)
   # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank = True)

    def __str__(self):
        '''return a string representation of a model instance'''

        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def get_all_comments(self):
        comments = Comment.objects.filter(article=self)
        return comments

class Comment(models.Model):
    '''comment about an article'''
    article = models.ForeignKey(Article, on_delete= models.CASCADE)
    author = models.TextField(blank = False)
    text = models.TextField(blank = False)
    published = models.DateTimeField(auto_now = True)

    def __str__(self):
        '''string rep of comment'''
        return f'{self.text}'