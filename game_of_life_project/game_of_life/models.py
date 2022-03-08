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
    SMALL, MEDIUM, LARGE = "S", "M", "L"
    STATE_DIM_CHOICES = [(SMALL, "Small"),(MEDIUM, "Small"),(LARGE, "Small")]

    date_created = models.DateTimeField()
    state_dimmentions = models.CharField(
        max_length=1,
        choices=STATE_DIM_CHOICES,
        default=MEDIUM,
    )
    state = models.TextField()

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(InitialState, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    states = models.TextField() # We need a way to store a bunck of states, use json

    def __str__(self):
        return self.user.username
    