from cgitb import small
from ctypes.wintypes import SMALL_RECT
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import json

NAME_MAX_LENGTH = 128
X_NODES = 100
Y_NODES = 100

class InitialState(models.Model):
    author = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    NAME_MAX_LENGTH = 128

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    SMALL, MEDIUM, LARGE, EXTRA  = 50, 100, 200, 300
    COL_COUNT_CHOICES = [
        (SMALL, "Small"),(MEDIUM, "Medium"),
        (LARGE, "Large"), (EXTRA, "Extra large")
        ]

    col_count = models.IntegerField(
        choices=COL_COUNT_CHOICES,
        default=MEDIUM,
    )
    state = models.TextField() # 2d array -> string (JSON)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(InitialState, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    states = models.TextField(blank=True) # We need a way to store a bunck of states, use json

    def __str__(self):
        return self.user.username
    