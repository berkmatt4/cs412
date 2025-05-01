from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Vehicle)
admin.site.register(Salesperson)
admin.site.register(Customer)
admin.site.register(SalesMatch)
admin.site.register(SalespersonReview)


#registering all of our models to use in the admin tool