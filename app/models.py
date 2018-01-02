from django.contrib.auth.models import User
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class friends(models.Model):
    id = models.intField()
    id_first = models.intField()
    id_second = models.intField()
    time_sent = models.intField()
    accepted = models.intField()
