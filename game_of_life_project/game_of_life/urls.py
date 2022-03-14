from django.urls import path
from game_of_life import views

app_name = 'game_of_life'

urlpatterns = [
     path('', views.index, name='index'),
     path('login/', views.user_login, name='login'),
     path('login_error/', views.user_login_error, name='login_error'),
     path('logout/', views.user_logout, name='logout'),
     path('register/', views.register, name='register'),
     path('game_logic/', views.game_logic, name='game_logic'),
     path('interesting_patterns/', views.interesting_patterns, name='interesting_patterns'),
     path('about/', views.about, name='about'),
     path('all_initial_states/', views.all_initial_states, name='all_initial_states'),
     path('profile/<username>/', views.profile, name='profile'),
     path('profile/<username>/create_initial_state/', views.create_initial_state, name='create_initial_state'),
     path('profile/<username>/initial_states/<slug:state_name_slug>', views.initial_state, name='initial_state'),
     path('create_add_pattern', views.create_add_pattern, name='create_add_pattern'),
    ]
