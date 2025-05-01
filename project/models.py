#models for the final project (car dealership)
#contains definitions for Vehicles, Customers, Salespeople
#SalesMatches (pending sales), SalesReviews
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Vehicle(models.Model):
    '''model representing a vehicle at the car dealership
    includes VIN, make, model, year, body type (SUV, sedan, etc)
    , engine size (num cylinders), average MPG, and msrp and a field for 
    determining if the vehicle is sold'''

    vin = models.TextField(blank = False)
    make = models.TextField(blank = False)
    model = models.TextField(blank = False)
    year = models.IntegerField(blank = False)
    body_type = models.TextField(blank = False)
    engine_size = models.IntegerField(blank = False)
    mpg = models.IntegerField(blank = False)
    msrp = models.IntegerField(blank = False)
    image = models.ImageField(blank = True)
    isSold = models.BooleanField(default = False)   #set a default value for new vehicles

def load_data():
    '''a function to create model instances from a 
    csv (Vehicle)
    The CSV used included 17 makes, each having multiple objects of the
    same vehicle to save time while creating a populous database'''
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

def load_images():
    '''a function to assign images to vehicles
    this is only used for vehicles created from the csv
    Since each initial vehicle would be duplicate vehicles of the same make,
    we can assign this based solely on the vehicles make'''

    makes = Vehicle.objects.values_list('make', flat = True).distinct() #grab the list of all vehicle makes

    for make in makes:
        image_path = f'vehicles/{make.lower()}.jpg'     #all images used were just <make>.jpg
        
        #grab all vehicles of the current make, and update their images
        vehicles = Vehicle.objects.filter(make=make)
        updated = vehicles.update(image=image_path)

        print(f'Updated {updated} vehicles of make {make} with image {image_path}')
    
    #see how many vehicles have no images
    vehicles_no_image = Vehicle.objects.filter(image='').count()
    print(f'Done. {vehicles_no_image} vehicles could not get an image')



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
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def get_sales_match(self):
        '''return the salesmatch associated with this customer'''
        try:
            return SalesMatch.objects.get(customer=self)    #return salesmatches relating to this customer
        except:
            return None
        
    def get_absolute_url(self):
        '''method to direct newly registered users to their page'''
        return reverse('customer_details', kwargs = {'pk': self.pk})    #after creation, display current user

class Salesperson(models.Model):
    '''a model representing a salesperson at the dealership
    includes full name and years working at the company'''

    first_name = models.TextField(blank = False)
    last_name = models.TextField(blank = False)
    years_working = models.IntegerField(blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        '''method to direct the salesperson to the team list after creation'''
        return reverse('salesperson_details', kwargs={'pk': self.pk})    #after creation, display the user
    
    def get_reviews(self):
        '''accessor to return the reviews of a specific salesperson'''

        review = SalespersonReview.objects.filter(salesperson = self)      #grab all reviews relating to this salesperson

        return review
    
    def get_average_rating(self):
        '''a function to return the average review rating of a salesperson'''

        reviews = SalespersonReview.objects.filter(salesperson = self)

        if reviews:
            rating = 0

        #loop through all reviews, then average them out
            for r in reviews:
                rating += r.rating
            
            rating = rating / len(reviews)

            return round(rating, 1)
        else:
            return -1       #return -1 if there are no reviews, so we can determine this later in views

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
    rating = models.FloatField(blank = False, validators=[      #including some validators to ensure that the rating is from 1-5 inclusive
        MaxValueValidator(5.0),
        MinValueValidator(1.0)
    ])
    review_text = models.TextField(blank = False)
