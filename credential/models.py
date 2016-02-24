from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UberCredential(models.Model):
    user = models.OneToOneField(User)
    authorization_code = models.CharField(max_length=512)
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expires_in = models.IntegerField()
    scope = models.CharField(max_length=512)
    created_date = models.DateField()

    def __unicode__(self):
        return self.user.username

