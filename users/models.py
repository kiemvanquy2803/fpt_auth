from django.db import models

from base.models import AbstractBaseUser

# Create your models here.


class Users(AbstractBaseUser):

    email = models.CharField(max_length=255, null=True, default=True)
