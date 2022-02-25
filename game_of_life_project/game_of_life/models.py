from django.db import models
from django.contrib.postgres.fields import ArrayField#####
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

NAME_MAX_LENGTH = 128
X_NODES = 100
Y_NODES = 100

class InitialState(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    date_created = models.DateTimeField()

    state = ArrayField(ArrayField(
            models.BooleanField(default=False),size=X_NODES,),
            size=Y_NODES,
            )

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

    states = models.ArrayField()

    def __str__(self):
        return self.user.username
    