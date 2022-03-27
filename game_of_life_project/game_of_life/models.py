import email
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from uuid import uuid4


import json
import os


class InitialState(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    NAME_MAX_LENGTH = 128

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    state = models.TextField()  # 2d array -> string (JSON)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(InitialState, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class InterestingPatten(models.Model):
    state = models.TextField()
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(InterestingPatten, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moderator = models.BooleanField(default=False)

    # # The additional attributes we wish to include.
  # Images renaming
    def path_and_rename(instance, filename):
        upload_to = 'profile_images'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    picture = models.ImageField(blank=True, upload_to=path_and_rename)
    likes= models.IntegerField(default=0)
    
    states = models.TextField(blank=True)  # We need a way to store a bunck of states, use json

    def __str__(self):
        return f'{self.user} Profile'



class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name="+")


class LikedAndSaved(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(InitialState, related_name="+")
    saved = models.ManyToManyField(InitialState, related_name="+")