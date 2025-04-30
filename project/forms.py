from django import forms
from .models import *

#a file to provide forms for the project app
#so far, it allows the salespeople to create salesmatch objects

class CreateSalesmatchForm(forms.ModelForm):
    '''A form which allows the salesperson to offer a price to an
    interested customer'''

    class Meta:
        model = SalesMatch
        fields = ['price']
        help_texts = {
            'price': "Enter a price in dollars",
        }

class CreateSalespersonReviewForm(forms.ModelForm):
    '''a form which allows customers to submit reviews for salespeople'''

    class Meta:
        '''associate our form with a model in the DB'''
        model = SalespersonReview

        fields = ['rating', 'review_text']

class UpdateSalesmatchForm(forms.ModelForm):
    '''a form for updating the price of a salesmatch'''

    class Meta:
        '''associate form with model in our db and provide updatable
        fields'''

        model = SalesMatch

        fields = ['price']
        help_texts = {
            'price': 'Enter an updated price'
        }

class OfferDecisionForm(forms.ModelForm):
    '''a form to allow customers to accept or reject the sales
        offer'''
    
    decisions = [
        ('accept', 'Accept Offer'),
        ('reject', 'Reject Offer and continue searching')
    ]
    decision = forms.ChoiceField(choices = decisions, widget = forms.RadioSelect)

    class Meta:
        model = SalesMatch
        fields = ['decision']

class CreateCustomerForm(forms.ModelForm):
    '''a form which allows the creation of a new customer'''

    class Meta:
        '''associate our form with a model in our DB'''

        model = Customer

        fields = ['first_name', 'last_name', 'credit_score', 'license_id']

class CreateSalespersonForm(forms.ModelForm):
    '''a form to create a new salesperson'''
    passkey = forms.CharField(max_length = 50, required = True, widget = forms.PasswordInput)

    class Meta:
        '''associate with a model and provide fields
        includes a new field for a secret passkey to prevent
        random people from registering as a salesperson'''
        model = Salesperson

        fields = ['first_name', 'last_name', 'years_working']

class CreateVehicleForm(forms.ModelForm):
    '''a form to create a new vehicle'''

    class Meta:
        '''associating our form with model and providing fields'''

        model = Vehicle

        fields = ['vin', 'make', 'model', 'year', 'body_type', 'engine_size', 'mpg', 'msrp', 'image']

class CreateSalespersonReviewForm(forms.ModelForm):
    '''a form to allow customers to submit reviews for salespeople'''

    class Meta:
        '''associating with SalespersonReview model and adding fields'''

        model = SalespersonReview

        fields = ['rating', 'review_text']

class UpdateSalesReviewForm(forms.ModelForm):
    '''a form to update a review'''

    class Meta:
        '''associatatng with a model in our db'''

        model = SalespersonReview

        fields = ['rating', 'review_text']
