from django.db import models


# Create your models here.


class RequiredKey(models.Model):
    user_key = models.CharField(max_length=30)




