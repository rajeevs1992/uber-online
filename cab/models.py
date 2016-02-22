from __future__ import unicode_literals

from django.db import models

class CabType(models.Model):
    name = models.CharField(max_length=100)
    min_fare = models.FloatField()
    min_fare_distance = models.FloatField()
    fare_per_km = models.FloatField()
    fare_per_min = models.FloatField()

    def __unicode__(self):
        return self.name
