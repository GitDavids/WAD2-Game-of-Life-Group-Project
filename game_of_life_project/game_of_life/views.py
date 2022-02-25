from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from game_of_life.models import Category, Page
from game_of_life.forms import UserForm, UserProfileForm #, CategoryForm, PageForm, 

from datetime import datetime


# Main page
def index(request):
    context_dict = {}

    return render(request, 'game_of_life/index.html', context=context_dict) # TODO


# Account pages
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                    login(request, user)
                    return redirect(reverse('game_of_life:index'))
            else:
                    return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'game_of_life/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('game_of_life:index'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,'game_of_life/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})



# Miscellaneous pages
def game_logic(request):
    context_dict = {}

    return render(request, 'game_of_life/game_logic.html', context=context_dict) # TODO

def interesting_patterns(request):
    context_dict = {}

    return render(request, 'game_of_life/interesting_patterns.html', context=context_dict) # TODO

def about(request):
    context_dict = {}

    return render(request, 'game_of_life/about.html', context=context_dict) # TODO

def all_initial_states(request):
    context_dict = {}

    return render(request, 'game_of_life/all_initial_states.html', context=context_dict) # TODO


# User specific pages
def user_account(request, user_slug):
    context_dict = {}

    return render(request, 'game_of_life/user_account.html', context=context_dict) # TODO

def create_initial_state(request, user_slug):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict) # TODO

def user_initial_states(request, user_slug):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict) # TODO


# Specific state
def state(request, user_slug, state_name_slug):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict) # TODO


# Moderator page
def create_add_pattern(request):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict)# TODO



