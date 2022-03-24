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

"""
All: structural tests
"""
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
        Checks whether the game_of_life app has been created.
        """
        directory_exists = os.path.isdir(self.game_of_life_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.game_of_life_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.game_of_life_app_dir, 'views.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The game_of_life app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The game_of_life directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The game_of_life directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_game_of_life_has_urls_module(self):
        """
        Checks the separate urls.py module for game_of_life
        """
        module_exists = os.path.isfile(os.path.join(self.game_of_life_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The game_of_life app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")

    def test_is_game_of_life_app_configured(self):
        """
        Checks the new game_of_life app is added to the INSTALLED_APPS list
        """
        is_app_configured = 'game_of_life' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The game_of_life app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")


"""
View: index
"""
class IndexTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the index() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'index' view named twice -- it should resolve to '/rango/'.
        """
        index_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True

        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:index'), '/game_of_life/', f"{FAILURE_HEADER}The index URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")

    def test_for_most_liked_and_recent_states_displaying(self):

        response = self.client.get(reverse('rango:index'))

        title = '<h1>Most liked states</h1>' in response.content.decode()
        title2 = '<h1>Most recent states</h1>' in response.content.decode()
        grid = '<div class="state_grid">' in response.content.decode() and '<div class="state_wrap">' in response.content.decode()
        statebox = '<a id="state1" href="http://127.0.0.1:8000/game_of_life/profile/Ashraf/initial_state/state1"><canvas class="state" width="400" height="200"></canvas></a>' in response.content.decode()
        statedescription = '<a class="state_description"' in response.content.decode()
        statejavascript = '<script>state_list.push(JSON.parse(' in response.content.decode()

        self.assertTrue(title, f"{FAILURE_HEADER}We couldn't find the Most Liked title in your index (home) page.{FAILURE_FOOTER}")
        self.assertTrue(title, f"{FAILURE_HEADER}We couldn't find the Most Liked title in your index (home) page.{FAILURE_FOOTER}")
        self.assertTrue(grid, f"{FAILURE_HEADER}We couldn't find the state display grid in your index (home) page.{FAILURE_FOOTER}")
        self.assertTrue(statebox, f"{FAILURE_HEADER}We couldn't find state1 in your index (home) page.{FAILURE_FOOTER}")
        self.assertTrue(statedescription, f"{FAILURE_HEADER}We couldn't find a state description in your index (home) page.{FAILURE_FOOTER}")
        self.assertTrue(statejavascript, f"{FAILURE_HEADER}We couldn't find state javascript in your index (home) page.{FAILURE_FOOTER}")

    def test_for_most_liked_and_recent_states_displaying_correctly_in_order(self):

        """im thinking create a state first to test the recent state"""
        """like a state to test the liked states"""


"""
View: user_login
"""
class LoginTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'user_login' in self.views_module_listing
        is_callable = callable(self.views_module.user_login)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The user_login() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the user_login() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'user_login' view named twice -- it should resolve to '/rango/'.
        """
        user_login_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'login':
                    user_login_mapping_exists = True

        self.assertTrue(user_login_mapping_exists, f"{FAILURE_HEADER}The login URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:login'), '/game_of_life/login/', f"{FAILURE_HEADER}The user_login URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")

"""
View: user_login_error 
"""

"""
View: user_logout (login required)
"""

"""
View: register
"""
class RegisterTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'register' in self.views_module_listing
        is_callable = callable(self.views_module.register)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The register() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the register() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'register' view named twice -- it should resolve to '/rango/'.
        """
        register_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'register':
                    register_mapping_exists = True

        self.assertTrue(register_mapping_exists, f"{FAILURE_HEADER}The register URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:register'), '/game_of_life/register/', f"{FAILURE_HEADER}The register URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: game_logic
"""
class GameLogicTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'game_logic' in self.views_module_listing
        is_callable = callable(self.views_module.game_logic)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The game_logic() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the game_logic() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'game_logic' view named twice -- it should resolve to '/rango/'.
        """
        game_logic_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'game_logic':
                    game_logic_mapping_exists = True

        self.assertTrue(game_logic_mapping_exists, f"{FAILURE_HEADER}The game_logic URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:game_logic'), '/game_of_life/game_logic/', f"{FAILURE_HEADER}The game_logic URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: interesting_patterns
"""
class InterestingPatternsTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'interesting_patterns' in self.views_module_listing
        is_callable = callable(self.views_module.interesting_patterns)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The interesting_patterns() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the interesting_patterns() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'interesting_patterns' view named twice -- it should resolve to '/rango/'.
        """
        interesting_patterns_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'interesting_patterns':
                    interesting_patterns_mapping_exists = True

        self.assertTrue(interesting_patterns_mapping_exists, f"{FAILURE_HEADER}The interesting_patterns URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:interesting_patterns'), '/game_of_life/interesting_patterns/', f"{FAILURE_HEADER}The interesting_patterns URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")

"""
View: patterns DOES NOT HAVE ANY PATTERNS SINCE THIS IS MODERATOR ADDED PATTERNS ONLY
"""
"""
class PatternsTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

        populate()
        self.response = self.client.get(reverse('rango:patterns', kwargs={'category_name_slug': 'other-frameworks'}))

    def test_view_exists(self):
        name_exists = 'pattern' in self.views_module_listing
        is_callable = callable(self.views_module.pattern)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The pattern() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the pattern() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
    
        patterns_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'pattern':
                    patterns_mapping_exists = True

        self.assertTrue(patterns_mapping_exists, f"{FAILURE_HEADER}The pattern URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('rango:patterns', kwargs={'category_name_slug': 'other-frameworks'}), 'interesting_patterns/<slug:pattern_name_slug>', f"{FAILURE_HEADER}The patterns URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
"""

"""
View: about
"""
class AboutTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The about() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the about() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'about' view named twice -- it should resolve to '/rango/'.
        """
        about_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'about':
                    about_mapping_exists = True

        self.assertTrue(about_mapping_exists, f"{FAILURE_HEADER}The about URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:about'), '/game_of_life/about/', f"{FAILURE_HEADER}The about URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: all_initial_states
"""
class AllInitialTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'all_initial_states' in self.views_module_listing
        is_callable = callable(self.views_module.all_initial_states)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The all_initial_states() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the all_initial_states() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'all_initial_states' view named twice -- it should resolve to '/rango/'.
        """
        all_initial_states_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'all_initial_states':
                    all_initial_states_mapping_exists = True

        self.assertTrue(all_initial_states_mapping_exists, f"{FAILURE_HEADER}The all_initial_states URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:all_initial_states'), '/game_of_life/all_initial_states/', f"{FAILURE_HEADER}The all_initial_states URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: profile (three ways: logged out, logged in and unfriended, friended)
"""

"""
View: create_initial_states (login required)
"""

"""
View: initial_states
"""
class InitialStateTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'initial_state' in self.views_module_listing
        is_callable = callable(self.views_module.initial_state)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The initial_state() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the initial_state() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        initial_state_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'initial_state':
                    initial_state_mapping_exists = True

        self.assertTrue(initial_state_mapping_exists, f"{FAILURE_HEADER}The initial_state URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:initial_state', kwargs={'username': 'Ashraf', 'state_name_slug': 'state2'}), '/game_of_life/profile/Ashraf/initial_state/state2', f"{FAILURE_HEADER}The initial_state URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: state
"""
class StateTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'state' in self.views_module_listing
        is_callable = callable(self.views_module.state)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The state() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the state() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'state' view named twice -- it should resolve to '/rango/'.
        """
        state_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'state':
                    state_mapping_exists = True

        self.assertTrue(state_mapping_exists, f"{FAILURE_HEADER}The state URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:state'), '/game_of_life/state/', f"{FAILURE_HEADER}The state URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")


"""
View: create_add_pattern
"""
class CreateAddPatternsTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('game_of_life.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('game_of_life.urls')

    def test_view_exists(self):
        name_exists = 'create_add_pattern' in self.views_module_listing
        is_callable = callable(self.views_module.create_add_pattern)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The create_add_pattern() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the create_add_pattern() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'create_add_pattern' view named twice -- it should resolve to '/rango/'.
        """
        create_add_pattern_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'create_add_pattern':
                    create_add_pattern_mapping_exists = True

        self.assertTrue(create_add_pattern_mapping_exists, f"{FAILURE_HEADER}The create_add_pattern URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('game_of_life:create_add_pattern'), '/game_of_life/create_add_pattern/', f"{FAILURE_HEADER}The create_add_pattern URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
