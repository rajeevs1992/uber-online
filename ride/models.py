from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=64)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Request(models.Model):
    user = models.ForeignKey(User)
    from_latitude = models.CharField(max_length=128)
    from_longitude = models.CharField(max_length=128)
    to_latitude = models.CharField(max_length=128)
    to_longitude = models.CharField(max_length=128)
    pending = models.BooleanField(default=True)
    book_date = models.DateField()
    
    requestid = models.CharField(max_length=512, null=True)
    productid = models.CharField(max_length=512, null=True)
    surge_confirmation_id = models.CharField(max_length=512, null=True)

    def __unicode__(self):
        return self.user.username + '-' + str(self.book_date)

class BookingDetails:
    
    def __init__(self, details):
        self.status = details['status']
        self.requestid = details['request_id']
        self.driver = details['driver']
        self.eta = details['eta']
        self.location = details['location']
        self.vehicle = details['vehicle']
        self.surge = details['surge_multiplier']
