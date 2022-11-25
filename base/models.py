import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from rest_framework.validators import ValidationError

# Create your models here.


class AbstractUserManager(UserManager):

    def get_auth_jwt(self, jwt_data):
        user = self.filter(
            email=jwt_data['email'],
            is_deleted=False
        ).first()
        if user:
            return user
        else:
            raise ValidationError(dict(
                message="The email/password you've entered in incorrect, please try again."
            ))

class AbstractBaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255, null=True, unique=True)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.UUIDField(null=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.UUIDField(null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.UUIDField(null=True)

    objects = AbstractUserManager()

    class Meta:
        abstract = True