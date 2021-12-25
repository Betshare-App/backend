from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class UserDocs(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    RG = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True)
    CPF = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20)

class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    street = models.CharField(max_length=200)
    quarter = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    state =  models.CharField(max_length=200)

class UserFinanceInfo(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    bank = models.CharField(max_length=50, null=True, blank=True)
    agency =  models.CharField(max_length=50, null=True, blank=True)
    account = models.CharField(max_length=50, null=True, blank=True)
    balance = models.FloatField(blank=True, null=True, default=0)
    pix_key = models.CharField(max_length=255, null=True, blank=True)
    
