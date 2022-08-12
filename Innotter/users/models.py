from django.contrib.auth.models import AbstractUser
from django.db import models
from pages.models import Post


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80, default="User")
    is_blocked = models.BooleanField(default=False)
    favourite_posts = models.ManyToManyField("pages.Post", related_name="favourites", blank=True)
