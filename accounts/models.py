from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    # add additional fields in here
    name_of_the_school = models.CharField(max_length=30, unique=False)
    username = models.CharField(max_length=20, unique=True)

    role = models.CharField(max_length=2)

    # contact
    email_address = models.EmailField(blank=False, null=False)  # require
    phone_number = models.CharField(max_length=10)

    # Registration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # When user create must need to fill this field
    REQUIRED_FIELDS = ["name_of_the_school", "role", "email_address", 'phone_number']

    def __str__(self):
        return self.username
    def permision(self):
        return self.role


class Selection(models.Model):
    ch_list = [
        ('ad', 'Signup as administrator'),
        ('te', 'Signup as teacher')
    ]
    Select_Role = models.CharField(choices=ch_list, max_length=2)
