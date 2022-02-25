import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_of_life_project.settings')

import django
django.setup()
from game_of_life.models import *

def populate():
    pass

# Start execution here!
if __name__ == '__main__':
    print('Starting Game of Life population script...')
    populate()
