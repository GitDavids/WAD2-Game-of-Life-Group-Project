from django import forms
from game_of_life.models import UserProfile, InitialState, InterestingPatten
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class InitialStateForm(forms.ModelForm):
    name = forms.CharField(max_length=InitialState.NAME_MAX_LENGTH,
                        help_text="Please enter the states name.")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    state = forms.CharField(help_text="or paste in a 2d array manually")
    class Meta:
        model = InitialState
        fields = ('state','name',)

    
class InterestingPatternForm(forms.ModelForm):
    name = forms.CharField(max_length=InterestingPatten.NAME_MAX_LENGTH,
                        help_text="Please enter the states name.")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    state = forms.CharField(help_text="or enter state manually.")

    class Meta:
        model = InterestingPatten
        fields = ('state','name',)





