from django.db import models
from django.contrib.auth.models import User
import uuid
# from core.models import Company


# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=100,default='user')

    def __str__(self):
        return self.user.username
    


    


