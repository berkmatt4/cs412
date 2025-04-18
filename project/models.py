#models for the final project (car dealership)
#contains definitions for Vehicles, Customers, Salespeople
#SalesMatches (pending sales), SalesReviews, CarReviews
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Vehicle(models.Model):
    '''model representing a vehicle at the car dealership
    includes VIN, make, model, year, body type (SUV, sedan, etc)
    , engine size (num cylinders), average MPG, and msrp'''

    vin = models.TextField(blank = False)
    make = models.TextField(blank = False)
    model = models.TextField(blank = False)
    year = models.IntegerField(blank = False)
    body_type = models.TextField(blank = False)
    engine_size = models.IntegerField(blank = False)
    mpg = models.IntegerField(blank = False)
    msrp = models.IntegerField(blank = False)
    image = models.ImageField(blank = True)

def load_data():
    '''a function to create model instances from a 
    csv (Vehicle)'''
    #delete all entries to prevent duplication
    Vehicle.objects.all().delete()

    filename = 'C:/Users/user/Documents/cars.csv'
    f = open(filename)
    f.readline()    #skip headers

    for line in f:
        fields = line.split(',')

        try:
            #create a new instance of the Vehicle using the current fields
            vehicle = Vehicle(make = fields[0],
                              model = fields[1],
                              year = fields[2],
                              body_type = fields[3],
                              engine_size = fields[4],
                              mpg = fields[5],
                              vin = fields[6],
                              msrp = fields[7].strip(),     #make sure we don't include newline characters
                              )
            vehicle.save() #commit to DB

        except:
            print(f'Skipped: {fields}') #catch any errors
    print(f'Done. Created {len(Vehicle.objects.all())} Vehicles')

class Customer(models.Model):
    '''model representing a customer at the car dealership
    includes full name, drivers license id, credit score,
    date of birth, and a foreign key reference to the vehicle
    they are interested in (if any)'''
    
    first_name = models.TextField(blank = False)
    last_name = models.TextField(blank = False)
    credit_score = models.IntegerField(blank = True)
    license_id = models.IntegerField(blank = False)
    interested_in = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

class Salesperson(models.Model):
    '''a model representing a salesperson at the dealership
    includes full name and years working at the company'''

    first_name = models.TextField(blank = False)
    last_name = models.TextField(blank = False)
    years_working = models.IntegerField(blank = True)

class SalesMatch(models.Model):
    '''a model representing a sale in progress
    includes a foreign key reference to a salesperson and 
    a customer, also includes the price as set by the salesperson'''

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    price = models.IntegerField(blank = False)

class SalespersonReview(models.Model):
    '''a model to hold reviews of a specific salesperson
    includes a foreign key to the customer submitting the review,
    a foreign key to the salesperson being reviewed, a rating from
    1-5 as an integer, and some text for the review body'''

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    rating = models.IntegerField(blank = False)
    review_text = models.TextField(blank = False)

class VehicleReview(models.Model):
    '''a model to hold reviews of a specific car. includes
    a foreign key to the car being reviewed, customer submitting review,
    also includes a rating as an integer, some text for the review body
    and the ability to put an image of the car'''

    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(blank = False)
    review_text = models.TextField(blank = False)
    car_image = models.ImageField(blank = True)     #image will be optional