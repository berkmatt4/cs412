from django.db import models

# Create your models here.
class Voter(models.Model):
    '''A class to represent a voter object
    Includes names, addresses, birthdays, registration date
    party affiliation, and precinct number'''

    #identification and address
    vid = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.IntegerField()
    dob = models.DateField()

    #voter info
    registration_date = models.DateField()
    party = models.CharField(max_length=2)
    precinct = models.IntegerField()

    #recent voting info
    #while all the first 5 are booleans, they are not formatted properly so i will store them as strings
    v20_state = models.TextField()
    v21_town = models.TextField()
    v21_primary = models.TextField()
    v22_general = models.TextField()
    v23_town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''return a string representation of a voter'''
        return f'{self.first_name} {self.last_name}, {self.party}, {self.zip_code}'
    
def load_data():
    '''function to create a model instance from each line of the CSV file'''

    #prevent duplicates
    Voter.objects.all().delete()

    filename = '/Users/user/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline()        #skip over the headers (descriptors)

    for line in f:
        fields = line.split(',')

        try:
            #create a new instance of a Voter with the current record
            voter = Voter(vid = fields[0],
                          last_name = fields[1],
                          first_name = fields[2],
                          street_number = fields[3],
                          street_name = fields[4],
                          apartment_number = fields[5],
                          zip_code = fields[6],
                          dob = fields[7],
                          registration_date = fields[8],
                          party = fields[9],
                          precinct = fields[10],
                          v20_state = fields[11],
                          v21_town = fields[12],
                          v21_primary = fields[13],
                          v22_general = fields[14],
                          v23_town = fields[15],
                          voter_score = fields[16].strip(),
                          )
            voter.save()        #commit to db

        except:
            print(f'Skipped: {fields}')     #error catching

    print(f'Done. Created {len(Voter.objects.all())} Voters')


