from django.contrib import admin
from game_of_life.models import UserProfile, InitialState, InterestingPatten

admin.site.register(InitialState)
admin.site.register(UserProfile)
admin.site.register(InterestingPatten)
