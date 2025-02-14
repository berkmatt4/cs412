from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
from datetime import datetime, timedelta

#views.py creates the logic for displaying templates, gathering info
#and regurgitating that info to the user!

# Create your views here.
def main(request):
    """view to show the main restaurant webpage"""

    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order(request):
    """view to allow the user to order something"""

    template_name = 'restaurant/order.html'

    specials = [
        "Buffalo Chicken Wrap, 12.99",
        "Chicken Caesar Wrap, 10.99",
        "Reuben Wrap, 14.99",
        "Philly Cheesesteak Wrap, 13.99"
    ]

    special = specials[random.randint(0, 3)]    #choose one of the specials at random

    #context dictionary for assigning the special
    context = {
        'special': special,
    }

    return render(request, template_name, context)

def confirmation(request: HttpRequest):
    """view to display confirmation after order"""

    print(request)

    current_time = datetime.now()
    now_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    time_change = timedelta(minutes=random.randint(30,60))

    ready_time = current_time + time_change
    ready_format = ready_time.strftime("%Y-%m-%d %H:%M:%S")

    #logic to grab all the posted data
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone-number')

        #check for each item
        ordered = request.POST.getlist('option')
        
        optional_ordered = request.POST.get('meat')
        if optional_ordered:
            optional_ordered = "Add "+optional_ordered
            ordered.append(optional_ordered)

        additional_comments = request.POST.get('additional')

        items = []
        cost = []

        print(ordered)
        #process the items
        for item in ordered:
            separate = item.split(",")
            print(item)
            items.append(separate[0])
            separate[1] = separate[1].strip()
            cost.append(float(separate[1]))

        total_cost = sum(cost)

        zipper_list = list(zip(items, cost))

        context = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "ordered_items": zipper_list,
            "order_cost": total_cost,
            "additional_comments": additional_comments,
            "time_ordered": now_time,
            "time_ready": ready_format
        }

        template_name = 'restaurant/confirmation.html'
        return render(request, template_name, context)

    else:
        template_name = 'restaurant/order.html'
        
        return render(request, template_name)


