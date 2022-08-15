from datetime import datetime
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField("pages.Tag", related_name="pages", blank=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="pages"
    )
    followers = models.ManyToManyField("users.User", related_name="follows", blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        "users.User", related_name="requests", blank=True
    )
    unblock_date = models.DateTimeField(null=True, blank=True)
    is_permamently_blocked = models.BooleanField(default=False)
    blacklisted_users = models.ManyToManyField("users.User", related_name="blacklisted", blank=True)
   
    def is_blocked_atm(self):
        return not (self.unblock_date == None or datetime.utcnow() > self.unblock_date)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey(
        "pages.Post", on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
