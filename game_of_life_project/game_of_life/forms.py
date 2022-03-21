from dataclasses import field
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
        fields = ('website', 'picture',)


class InitialStateForm(forms.ModelForm):
    name = forms.CharField(max_length=InitialState.NAME_MAX_LENGTH,
                        help_text="Please enter the states name.")
    # author = forms.CharField(widget=forms.HiddenInput(), required=False) # TODO
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)   # TODO

    class Meta:
        model = InitialState
        fields = ('author','name','col_count',)
    
class InterestingPatternForm(forms.ModelForm):
    name = forms.CharField(max_length=InitialState.NAME_MAX_LENGTH,
                        help_text="Please enter the states name.")
    # author = forms.CharField(widget=forms.HiddenInput(), required=False) # TODO
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)   # TODO

    class Meta:
        model = InterestingPatten
        fields = ('name','col_count',)

