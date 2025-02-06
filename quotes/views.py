from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time
# Create your views here.

quotes = [
    "Life is too short to do the things you don't love doing.",
    "If heavy metal bands ruled the world, we'd be a lot better off.",
    "Rock music should be gross: that's the fun of it. It gets up and drops its trousers.",
    "Major labels blow all their money massively and blame it on the band.",
    "Teachers need to be more inspirational. But it's also up to engineering to make itself more interesting.",
]

images = [
    "/quotes/images/bruce1.jpg",
    "/quotes/images/bruce2.jpg",
    "/quotes/images/bruce3.jpg",
    "/quotes/images/bruce4.jpg",
    "/quotes/images/bruce5.jpg",
]


def quote_page(request):
    """Defines a view for the base page and quote page"""

    template = "quotes/quote.html"

    #context randomly assigned to a quote and an image
    context = {
        'quote': quotes[random.randint(0,4)],
        'image': images[random.randint(0,4)],
        'current_time': time.ctime()
    }

    return render(request, template, context)

def all_page(request):

    template = "quotes/show_all.html"

    #context is now the whole list of quotes and images
    context = {
        'quotes': quotes,
        'images': images,
        "current_time": time.ctime()
    }

    return render(request, template, context)

def about_page(request):

    template = "quotes/about.html"

    context = {
        "current_time": time.ctime()
    }

    return render(request, template, context)