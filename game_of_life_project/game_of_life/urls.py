from django.urls import path
from game_of_life import views

app_name = 'game_of_life'

urlpatterns = [
     path('', views.index, name='index'),
     path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
     path('register/', views.register, name='register'),
     path('game_logic/', views.game_logic, name='game_logic'),
     path('interesting_patterns/', views.interesting_patterns, name='interesting_patterns'),
     path('about/', views.about, name='about'),
     path('all_initial_states/', views.all_initial_states, name='all_initial_states'),
     path('<slug:user_slug>/', views.user_account, name='user_account'),
     path('<slug:user_slug>/create_initial_state/', views.create_initial_state, name='create_initial_state'),
     path('<slug:user_slug>/initial_states', views.user_initial_states, name='user_initial_states '),
     path('<slug:user_slug>/initial_states/<slug:state_name_slug>', views.state, name='user'),
     path('create_add_pattern', views.create_add_pattern, name='create_add_pattern'),
    ]
