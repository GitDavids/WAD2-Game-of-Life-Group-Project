from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# from game_of_life.models import Category, Page
from game_of_life.models import InitialState
from game_of_life.forms import UserForm, UserProfileForm #, CategoryForm, PageForm, 

from datetime import datetime


# Main page
def index(request):
    context_dict = {}
    context_dict["liked_states"] = InitialState.objects.order_by('-likes')[:6]
    context_dict["recent_states"] = InitialState.objects.order_by('-views')[:6]
    
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
def profile(request, username):
    context_dict = {}
    try:
        user = User.objects.get(username=username)
        states = InitialState.objects.filter(author=user)
        context_dict['user'] = user
        context_dict['states'] = states
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['states'] = None
    return render(request, 'game_of_life/profile.html', context=context_dict)

def create_initial_state(request, user_slug):
    # https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method
    # form = FUNCTION(request.POST)
    # instance = form.save(commit=False)
    # instance.author = request.user
    # instance.save()
    context_dict = {}

    return render(request, 'game_of_life/create_initial_state.html', context=context_dict) # TODO

def user_initial_states(request, user_slug):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict) # TODO


# Specific state
def initial_state(request, user_slug, state_name_slug):
    context_dict = {}

    context_dict["state"] = None
    context_dict["name"] = None
    context_dict["author"] = None
    context_dict["likes"] = None

    return render(request, 'game_of_life/view_initial_state.html', context=context_dict) # TODO


# Moderator page
def create_add_pattern(request):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict)# TODO



