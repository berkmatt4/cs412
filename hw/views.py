from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time
# Create your views here.

def home(request):
    """
    Defines a view to handle the home request
    """

    response_text = f'''
    <html>
    <h1> Hello, world!</h1>
    The current time is {time.ctime()}.
    </html>
    '''
    return HttpResponse(response_text)

def home_page(request):
    """ Home page using template """

    template = 'hw/home.html'

    #add context dict
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65, 90)),
        'letter2': chr(random.randint(65,90)),
        'number': random.randint(1,10),
    }

    return render(request, template, context)

def about(request):
    """Define a view to show about.html"""

    template = 'hw/about.html'

    context = {
        'current_time': time.ctime(),
    }

    return render(request, template, context)

