import os, json, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_of_life_project.settings')

import django
django.setup()
from game_of_life.models import *

STATES = [
    {"name":"state1","col_count":100,
    "state":[[random.randint(0,1) for _ in range(100)]for _ in range(50)]},
    {"name":"state2","col_count":50,
    "state":[[random.randint(0,1) for _ in range(50)]for _ in range(25)]},
    {"name":"state3","col_count":200,
    "state":[[random.randint(0,1) for _ in range(200)]for _ in range(100)]},
    {"name":"state4","col_count":300,
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state5","col_count":300,
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state6","col_count":300,
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state7","col_count":300,
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
]
SETTINGS = [
    {"email_public": True},
    {"email_public": True},
    {"email_public": True},
    {"email_public": True},
    {"email_public": True},
    {"email_public": True},
]
USERS = [
    {"username":"Ashraf","states":STATES[:2],"setings":SETTINGS[0]},
    {"username":"GitDavids","states":STATES[2:3],"setings":SETTINGS[1]},
    {"username":"geontog","states":STATES[3:4],"setings":SETTINGS[2]},
    {"username":"LiliOak","states":STATES[4:5],"setings":SETTINGS[3]},
    {"username":"GoldenZs3","states":STATES[5:],"setings":SETTINGS[4]},
    {"username":"amorri40","states":[],"setings":SETTINGS[5]},
]

def populate():
    for user in USERS:
        add_user(user['username'], user['states'])
    
    # Print out the categories we have added.
    for p in UserProfile.objects.all():
        print(f'{p}, {p.states}')


    
def add_user(userInput, states, settings=None): # TODO (5 min of bodge attempt, hoped it would work :( )
    u = User.objects.get_or_create(username = userInput)[0]
    u.save()

    p = UserProfile.objects.get_or_create(user = u)[0]
    

    if settings:
        pass # TODO
    
    state_list = []
    for state in states:
        state_list.append(add_state(p.user, state["name"], state["state"], state["col_count"]))

    print(state_list)
    # p.states = json.dumps(state_list)   ????somehelp here


    p.save()
    return p

def add_state(user, title, state, col_count = 100, views=0, likes=0):# TODO (5 min of bodge attempt, hoped it would work :()
    s = InitialState.objects.get_or_create(author=user, name=title)[0]
    s.state = json.dumps(state)
    s.col_count = col_count
    s.views=views
    s.likes=likes
    s.save()
    return s

# Start execution here!
if __name__ == '__main__':
    print('Starting Game of Life population script...')
    populate()