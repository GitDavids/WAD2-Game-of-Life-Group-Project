import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
#
# Last updated: March 14th, 2022
#
# In order to run these tests, this module should be in your game_of_life_project/game_of_life/ directory
# To run $ python manage.py test game_of_life.tests
#
"""
•Tests should be arranged so they are kept manageable.
There should be:
    −a separate TestClass for each model or view
    −a separate test method for each set of conditions you want to test
    −intuitive test method names that should describe their function
"""

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}GoL TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):
    """
    Checks the file structure of the project and if game_of_life is in list of INSTALLED_APPS.
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.game_of_life_app_dir = os.path.join(self.project_base_dir, 'game_of_life')

    def test_project_created(self):
        """
        Checks the game_of_life_project configuration directory is present and correct.
        """
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'game_of_life_project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'game_of_life_project', 'urls.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your game_of_life_project configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")

    def test_game_of_life_app_created(self):
        """
        Determines whether the game_of_life app has been created.
        """
        directory_exists = os.path.isdir(self.game_of_life_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.game_of_life_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.game_of_life_app_dir, 'views.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The game_of_life app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The game_of_life directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The game_of_life directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_game_of_life_has_urls_module(self):
        """
        Did you create a separate urls.py module for game_of_life?
        """
        module_exists = os.path.isfile(os.path.join(self.game_of_life_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The game_of_life app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")

    def test_is_game_of_life_app_configured(self):
        """
        Did you add the new game_of_life app to your INSTALLED_APPS list?
        """
        is_app_configured = 'game_of_life' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The game_of_life app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")


"""
View: index
"""

"""
View: user_login
"""

"""
View: user_logout
"""

"""
View: register
"""

"""
View: game_logic
"""

"""
View: interesting_patterns
"""

"""
View: about
"""

"""
View: all_initial_states
"""

"""
View: user_account
"""

"""
View: create_initial_states
"""

"""
View: user_initial_states
"""

"""
View: state
"""

"""
View: create_add_pattern
"""