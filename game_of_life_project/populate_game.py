import os, json, random
from game_of_life_project.settings import STATIC_URL, BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_of_life_project.settings')

import django
django.setup()
from game_of_life.models import *

with open(f"{BASE_DIR}{STATIC_URL}population_script_states.json", "r") as json_file:
    data = json.load(json_file)
    
PATTERNS = data["patterns"]
STATES = [
    {"name":"state1",
    "state":[[0 for _ in range(100)]for _ in range(50)]},
    {"name":"state2",
    "state":[[random.randint(0,1) for _ in range(50)]for _ in range(25)]},
    {"name":"state3",
    "state":[[random.randint(0,1) for _ in range(200)]for _ in range(100)]},
    {"name":"state4",
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state5",
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state6",
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state7",
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state8",
    "state":[[random.randint(0,1) for _ in range(300)]for _ in range(150)]},
    {"name":"state9",
    "state":[[(i+j)%2 for i in range(300)]for j in range(150)]},
    {"name":"state10",
    "state":[[j % 2 for _ in range(300)]for j in range(150)]},
    {"name":"state11",
    "state":[[i % 2 for i in range(300)] for _ in range(150)]},
    {"name":"state12",
    "state":[[(i*j)%2 for i in range(300)] for j in range(150)]},
    {"name":"state13",
    "state":[[((i*j)%2+i)%2 for i in range(300)] for j in range(150)]},
]

SETTINGS = [
    {"email_public": True}, #0
    {"email_public": True}, #1
    {"email_public": True}, #2
    {"email_public": True}, #3
    {"email_public": True}, #4
    {"email_public": True}, #5
    {"email_public": True}, #6
]
USERS = [
    {"username":"Ashraf","states":STATES[:2],"setings":SETTINGS[0]},
    {"username":"GitDavids","states":data["states_by_David"],"setings":SETTINGS[1]},
    {"username":"geontog","states":STATES[2:4],"setings":SETTINGS[2]},
    {"username":"LiliOak","states":STATES[4:5],"setings":SETTINGS[3]},
    {"username":"GoldenZs3","states":STATES[5:6],"setings":SETTINGS[4]},
    {"username":"amorri40","states":STATES[6:7],"setings":SETTINGS[5]},
    {"username":"Marta","states":STATES[7:],"setings":SETTINGS[6]},
]

def populate():
    for user in USERS:
        add_user(user['username'], user['states'])
    
    # Print out the categories we have added.
    for p in UserProfile.objects.all():
        print(f'{p}, {p.states}')
    for p in PATTERNS:
        add_pattern(p['name'], p['state'])   


    
def add_user(userInput, states, settings=None): # TODO (5 min of bodge attempt, hoped it would work :( )
    u = User.objects.get_or_create(username = userInput)[0]
    u.save()

    p = UserProfile.objects.get_or_create(user = u)[0]
    

    if settings:
        pass # TODO
    
    state_list = []
    for state in states:
        state_list.append(add_state(p.user, state["name"], state["state"]))

    #print(state_list)
    # p.states = json.dumps(state_list)   ????somehelp here


    p.save()
    return p

def add_state(user, title, state, views=0, likes=0):# TODO (5 min of bodge attempt, hoped it would work :()
    s = InitialState.objects.get_or_create(author=user, name=title)[0]
    s.state = json.dumps(state)
    s.views=views
    s.likes=likes
    s.save()
    return s

def add_pattern(title, state):
    p=InterestingPatten.objects.get_or_create(name=title )[0]
    p.state = json.dumps(state)
    p.save()
    return p

# Start execution here!
if __name__ == '__main__':
    print('Starting Game of Life population script...')
    populate()