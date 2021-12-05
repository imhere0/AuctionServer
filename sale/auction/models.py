from typing import Callable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import NullBooleanField

# from auction.views import Listing


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length= 250)

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class ListingModel(models.Model):
    id = models.AutoField(primary_key= True)
    owner_id = models.ForeignKey(User, on_delete = CASCADE, null= True)
    owner = models.CharField(max_length=125)
    title = models.CharField(max_length= 125)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField(auto_now_add= True)
    image = models.ImageField(upload_to='nameFile', null = False)

class BidModel(models.Model):
    listingid = models.ForeignKey(ListingModel, on_delete= CASCADE)
    user_id = models.ForeignKey(User, on_delete = CASCADE)
    amount = models.IntegerField()

class CommentModel(models.Model):
    listingid = models.ForeignKey(ListingModel, on_delete= CASCADE)
    user_id = models.ForeignKey(User, on_delete = CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add= True)

class WinnerModel(models.Model):
    user_id = models.ForeignKey(User, on_delete = CASCADE)
    listingid = models.ForeignKey(ListingModel, on_delete = CASCADE)
    time = models.DateTimeField(auto_now_add= True)
