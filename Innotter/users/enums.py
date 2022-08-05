from django.db import models


class RolesEnum(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
