from django.contrib.auth.models import User
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Person(models.Model):
    name = models.charField();