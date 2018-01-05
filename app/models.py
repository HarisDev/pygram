from __future__ import unicode_literals
from django.contrib.auth.models import *
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(blank=True, default='username.png')

    class Meta:
        db_table = 'auth_user'

# Create your models here.

# class friends(models.Model):
#     id = models.intField()
#     id_first = models.intField()
#     id_second = models.intField()
#     time_sent = models.intField()
#     accepted = models.intField()
