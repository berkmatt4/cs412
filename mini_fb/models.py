#models for the mini_fb assignment
#contains definitions for Profiles, StatusMessages, Images, StatusImages

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''model for profiles on our mini_fb app
    text fields for f_name, l_name, city, and email
    url field for the image'''
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank = True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''return a string representation of the user's profile'''
        return f'{self.first_name} {self.last_name}'

    def get_status_message(self):
        '''accessor to return the status messages related to the profile'''
        status = StatusMessage.objects.filter(profile = self)

        #sorting status messages with most recent displayed first
        sorted_status = status.order_by('-published')

        return sorted_status
    
    def get_absolute_url(self):
        '''method to show the new record after creation'''

        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''method to get all friends of given profile'''

        #query the database to retrieve friend objects where either profile is self
        friends = Friend.objects.filter(profile1 = self) | Friend.objects.filter(profile2 = self)

        friendList = []

        #build the friend list
        #for each friendship, add to the list the profile which is not self
        for friend in friends:
            if friend.profile1 == self:
                friendList.append(friend.profile2)
            else:
                friendList.append(friend.profile1)
        
        return friendList

    def add_friend(self, other):
        '''method allowing the creation of a Friend relationship'''

        #user cannot friend themself
        if self == other:
            return #"Cannot friend self"
        #user cannot friend someone they are already friends with
        elif other in self.get_friends():
            return #"Users already friends"
        #otherwise, create the friend object
        else:
            friend = Friend()
            friend.profile1 = self
            friend.profile2 = other
            friend.save()
          #  return friend

    def get_friend_suggestions(self):
        '''method which returns friend suggestions (profile objects)
        for a given user'''
        #first grab all the friends of the user
        friends = self.get_friends()

        suggestions = []

        #for each friend, get their friends
        for friend in friends:
            friendsOfFriend = friend.get_friends()

            #for each friend of a friend, ensure they are not one of this person's friends already
            #then make sure they aren't already a suggested friend and that they aren't the person themself
            for person in friendsOfFriend:
                if not(person in friends) and not(person in suggestions) and not(person == self):
                    suggestions.append(person)

        print(suggestions)
        return suggestions

    def get_news_feed(self):
        '''method which returns a list of all the statusmessages associated 
        with the given profile as well as the friends of the profile'''

        friends = self.get_friends()
        #start with the status messages of the current profile
        newsQuerySet = StatusMessage.objects.filter(profile = self)

        #then, for each friend, query their status messages and then use the 
        #or operator to create a combined query set (similar to appending to a list)
        for friend in friends:
            tempQuery = StatusMessage.objects.filter(profile = friend)

            newsQuerySet = newsQuerySet | tempQuery
        
        #create an empty query set for status images
        statusImageSet = StatusImage.objects.none()

        #for each status message, find the associated status image and then or it to the empty set we made
        for news in newsQuerySet:
            tempQuery = StatusImage.objects.filter(status_message = news)

            statusImageSet = statusImageSet | tempQuery

        statusImageSet = statusImageSet.order_by('-status_message__published')
        print(statusImageSet)
        return statusImageSet
    

        


class StatusMessage(models.Model):
    '''model for creating status messages on our mini facebook
    includes a foreign key reference for the users Profile'''
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    message = models.TextField(blank = False)
    published = models.DateTimeField(auto_now = True)   #get the current time

    def __str__(self):
        '''create a string representation of a StatusMessage object'''
        return f'{self.message}'
    
    def get_images(self):
        '''function to retrieve all images associated with the model'''
        #getting all status images associated with this status message
        status_images = StatusImage.objects.filter(status_message = self)
        images = []
        for img in status_images:
            images.append(img.image_file)
        return images



class Image(models.Model):
    '''A model to store images as files
    Includes a foreign key to the Profile attached to the image'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  #foreign key reference for a profile
    image_file = models.ImageField(blank = False)
    timestamp = models.DateTimeField(auto_now = True)
    caption = models.TextField(blank=True)  #making this field optional

    def __str__(self):
        '''defining a toString method to print the image'''
        return f'{self.profile.first_name} image: {self.image_file}'
    
class StatusImage(models.Model):
    '''Representation of an image corresponding to a status message
    includes two foreign keys: image_file, and status_message'''

    image_file = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)


class Friend(models.Model):
    '''model which defines a relationship (friendship) between two profiles
    contains two Profile foreign keys and a timestamp for when the friendship
    began'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    anniversary = models.DateTimeField(auto_now = True)

    def __str__(self):
        '''method returning a string representation of a friendship'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'