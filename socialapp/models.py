from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, F, CheckConstraint
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    about = models.CharField(max_length=500, default="Lorem Ipsum")
    is_verified = models.BooleanField(default=False)

class UserFollowing(models.Model):
    to_follow = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    who_follows = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)

    class Meta:
        # prevents user from following user twice
        unique_together = ("to_follow", "who_follows")
        # prevents user from following themselves
        constraints = [
            CheckConstraint(check=~Q(who_follows=F('to_follow')), name='no_self_rating')
        ]

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "posts" , on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    image = models.URLField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    date_hidden = models.DateTimeField(blank=True, null=True)
    hidden_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hidden_by",on_delete=models.CASCADE, null=False) 

    def __str__(self):
        return self.text
class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "posts" , on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    date_hidden = models.DateTimeField(blank=True, null=True)
    hidden_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hidden_by",on_delete=models.CASCADE, null=False)
    reply_to = models.ForeignKey(Post, related_name="reply_to", on_delete=models.CASCADE, null=False)

class Report(models.Model):
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        # prevents user from liking post twice
        unique_together = ("user", "post")

class UserToUserConnection(models.Model):
    u1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="u1", on_delete=models.CASCADE)
    u2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="u2", on_delete=models.CASCADE)