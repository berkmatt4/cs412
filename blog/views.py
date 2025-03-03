#views for the blog app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
import random
from .forms import CreateArticleForm, CreateCommentForm, UpdateArtricleForm
from django.urls import reverse

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display one article'''

    model = Article
    template_name= "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):
    '''display single article at random'''

    model = Article
    template_name ="blog/article.html"
    context_object_name = "article"

    def get_object(self):
        '''return rando instance of article object'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class CreateArticleView(CreateView):
    '''display html form, process submission, create new article'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        return super().form_valid(form)

class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        
        pk = self.kwargs['pk']

        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):

        context = super().get_context_data()

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        context['article'] = article

        return context

    def form_valid(self, form):
        
        print(form.cleaned_data)

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        form.instance.article=article

        return super().form_valid(form)

class UpdateArticleView(UpdateView):

    model = Article
    form_class = UpdateArtricleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        
        #find pk of comment
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)


        #find pk of article 
        article = comment.article

        return reverse('article', kwargs = {'pk': article.pk})