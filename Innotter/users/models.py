from django.contrib.auth.models import AbstractUser
from django.db import models

from users.enums import RolesEnum


class User(AbstractUser):

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=RolesEnum.choices)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
