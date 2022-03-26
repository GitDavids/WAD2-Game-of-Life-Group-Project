from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View

from game_of_life.models import InitialState, UserProfile, InterestingPatten, FriendsList, LikedAndSaved
from game_of_life.forms import UserForm, UserProfileForm, InitialStateForm, InterestingPatternForm

from datetime import datetime


# Home page
def index(request):
    context_dict = {}
    context_dict["most_liked_states"] = InitialState.objects.order_by('-likes')[:6]
    context_dict["most_recent_states"] = InitialState.objects.order_by('-date_created')[:6]
    
    return render(request, 'game_of_life/index.html', context=context_dict) # TODO


# Account views
class Account(View):
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


# Profile views including states
class Profile(View):
    def profile(request, username):
        context_dict = {}

        try:
            if username == request.user.username:
                context_dict['thisMyPage'] = "true"

            user = User.objects.get(username=username)
            states = InitialState.objects.filter(author=user)
            context_dict['user'] = user
            context_dict['states'] = states

            try:
                friends = FriendsList.objects.get(user=user)
                context_dict['friends'] = friends.friends.all()
            except FriendsList.DoesNotExist:
                context_dict['friends'] = ""

            try:
                saved_and_liked_states = LikedAndSaved.objects.get(user=user)
                context_dict['liked_states'] = saved_and_liked_states.liked.all()
                context_dict['saved_states'] = saved_and_liked_states.saved.all()
            except LikedAndSaved.DoesNotExist:
                context_dict['liked_states'] = ""
                context_dict['saved_states'] = ""


            if request.user.is_authenticated:
                try:
                    requester_friends = FriendsList.objects.get(user=request.user)
                    context_dict['requester_friends'] = requester_friends.friends.all()
                except FriendsList.DoesNotExist:
                    context_dict['requester_friends'] = ""


        except User.DoesNotExist:
            context_dict['user'] = None
            context_dict['states'] = None


        return render(request, 'game_of_life/profile.html', context=context_dict)

    def add_friend(request, username):
        friend = User.objects.get(username=username)
        me = User.objects.get(username=request.user)


        my_friends = FriendsList.objects.get_or_create(user=me)[0]
        my_friends.save()
        my_friends.friends.add(friend)

        friend_friends = FriendsList.objects.get_or_create(user=friend)[0]
        friend_friends.save()
        friend_friends.friends.add(me)

        return redirect('game_of_life:profile', username=username)

    def remove_friend(request, username):
        friend = User.objects.get(username=username)
        me = User.objects.get(username=request.user)


        my_friends = FriendsList.objects.get_or_create(user=me)[0]
        my_friends.save()
        my_friends.friends.remove(friend)

        friend_friends = FriendsList.objects.get_or_create(user=friend)[0]
        friend_friends.save()
        friend_friends.friends.remove(me)

        return redirect('game_of_life:profile', username=username)

    #creation page
    @login_required
    def create_initial_state(request,username):
        context_dict = {}

        form = InitialStateForm()
        if request.method == 'POST':
            form = InitialStateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect(reverse('game_of_life:index'))
            else:
                print(form.errors)

        context_dict['form'] = form

        user = request.user
        context_dict['user'] = user
        return render(request, 'game_of_life/create_initial_state.html', context=context_dict) # TODO

    #completed state page:
    def initial_state(request, username, state_name_slug):
        context_dict = {}
        state = InitialState.objects.get(slug=state_name_slug)
        state.views +=1
        state.save()
        context_dict["state"] = state
        context_dict["name"] = state.name
        context_dict["author"] = state.author
        context_dict["username"] = username
        context_dict["state_name_slug"] = state_name_slug

        try:
            user = User.objects.get(username=request.user)
            context_dict['user'] = user
            user_liked_and_saved_states = LikedAndSaved.objects.get_or_create(user=user)[0]

            if state in user_liked_and_saved_states.liked.all():
                context_dict["user_already_liked"] = "true"
            else:
                context_dict["user_already_liked"] = None

            if state in user_liked_and_saved_states.saved.all():
                context_dict["user_already_saved"] = "true"
            else:
                context_dict["user_already_saved"] = None

        except User.DoesNotExist:
            context_dict['user'] = None

        return render(request, 'game_of_life/initial_state.html', context=context_dict) # TODO

    def like_state(request, username, state_name_slug):
        state = InitialState.objects.get(slug=state_name_slug)

        my_liked = LikedAndSaved.objects.get_or_create(user=request.user)[0]
        my_liked.save()
        my_liked.liked.add(state)

        state.likes += 1
        state.save()

        return redirect('game_of_life:initial_state', username=username, state_name_slug=state_name_slug)

    def unlike_state(request, username, state_name_slug):
        state = InitialState.objects.get(slug=state_name_slug)

        my_liked = LikedAndSaved.objects.get_or_create(user=request.user)[0]
        my_liked.save()
        my_liked.liked.remove(state)

        state.likes-=1
        state.save()

        return redirect('game_of_life:initial_state', username=username, state_name_slug=state_name_slug)

    def save_state(request, username, state_name_slug):
        state = InitialState.objects.get(slug=state_name_slug)

        my_saved = LikedAndSaved.objects.get_or_create(user=request.user)[0]
        my_saved.save()
        my_saved.saved.add(state)

        return redirect('game_of_life:initial_state', username=username, state_name_slug=state_name_slug)

    def unsave_state(request, username, state_name_slug):
        state = InitialState.objects.get(slug=state_name_slug)

        my_saved = LikedAndSaved.objects.get_or_create(user=request.user)[0]
        my_saved.save()
        my_saved.saved.remove(state)

        return redirect('game_of_life:initial_state', username=username, state_name_slug=state_name_slug)


# Moderator page
@login_required
def create_add_pattern(request):
    context_dict = {}

    form = InterestingPatternForm()

    if request.method == 'POST':
        form = InterestingPatternForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('game_of_life:index'))
        else:
            print(form.errors)

    context_dict['form'] = form

    return render(request, 'game_of_life/create_add_pattern.html', context=context_dict)# TODO

# Miscellaneous page views
def game_logic(request):
    context_dict = {}

    return render(request, 'game_of_life/game_logic.html', context=context_dict) # TODO

def interesting_patterns(request):
    context_dict = {}
    context_dict["patterns"] = InterestingPatten.objects.all()
    return render(request, 'game_of_life/interesting_patterns.html', context=context_dict) # TODO

def pattern(request, pattern_name_slug):
    context_dict = {}
    context_dict["pattern"] = InterestingPatten.objects.get(slug=pattern_name_slug)
    return render(request, 'game_of_life/pattern.html', context=context_dict) # TODO

def about(request):
    context_dict = {}

    return render(request, 'game_of_life/about.html', context=context_dict) # TODO

def all_initial_states(request):
    context_dict = {}
    context_dict["all_states"] = InitialState.objects.all()
    return render(request, 'game_of_life/all_initial_states.html', context=context_dict) # TODO



