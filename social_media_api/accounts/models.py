# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_profile_picture_upload_to(instance, filename):
    return f'profile_pics/user_{instance.id}/{filename}'

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_upload_to, blank=True, null=True)
    # followers: users who follow this user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',  # user.following -> QuerySet of users this user follows
        blank=True
    )

    def __str__(self):
        return self.username
