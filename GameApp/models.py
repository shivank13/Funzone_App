from django.db import models

# Create your models here.
from CoreApp.models import User


class Game(models.Model):
    room_code = models.CharField(max_length=100)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100)