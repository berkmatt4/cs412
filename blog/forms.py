from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an article to the db'''

    class Meta:
        '''associate form with model in db'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['author', 'text']