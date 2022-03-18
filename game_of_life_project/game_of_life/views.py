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
    context_dict["most_liked_states"] = InitialState.objects.order_by('-likes')[:6]
    context_dict["most_recent_states"] = InitialState.objects.order_by('-views')[:6]
    
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
            return redirect(reverse('game_of_life:login_error'))

    else:
        return render(request, 'game_of_life/login.html')

def user_login_error(request):
    context_dict = {}

    return render(request, 'game_of_life/login_error.html', context=context_dict) # TODO

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
    context_dict["all_states"] = InitialState.objects.all()
    return render(request, 'game_of_life/all_initial_states.html', context=context_dict) # TODO


# User specific pages
def profile(request, username):
    context_dict = {}
    try:
        user = User.objects.get(username=username)
        states = InitialState.objects.filter(author=user)
        context_dict['user'] = user
        context_dict['username'] = user.username
        context_dict['states'] = states
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['states'] = None
    return render(request, 'game_of_life/profile.html', context=context_dict)

def create_initial_state(request,username):
    context_dict = {}

    user = request.user
    context_dict['user'] = user
    return render(request, 'game_of_life/create_initial_state.html', context=context_dict) # TODO


# Specific state
def initial_state(request, username, state_name_slug):
    context_dict = {}
    state = InitialState.objects.get(slug=state_name_slug)
    context_dict["state"] = state
    context_dict["col_count"] = state.col_count
    context_dict["name"] = state.name
    context_dict["author"] = state.author
    context_dict["username"] = username
    context_dict["state_name_slug"] = state_name_slug

    return render(request, 'game_of_life/initial_state.html', context=context_dict) # TODO


# Moderator page
def create_add_pattern(request):
    context_dict = {}

    return render(request, 'game_of_life/REPLACE.html', context=context_dict)# TODO
