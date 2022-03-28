import os
from django.test import TestCase
from django.conf import settings
from game_of_life.models import UserProfile, InitialState, InterestingPatten, FriendsList, LikedAndSaved
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.images import ImageFile

# To run: $ python manage.py test game_of_life.tests

"""
•Tests should be arranged so they are kept manageable.
There should be:
    −a separate TestClass for each model or view
    −a separate test method for each set of conditions you want to test
    −intuitive test method names that should describe their function
"""

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}GoL TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

# Check everything set up okay - good just in case.

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
        Checks for models.py
        """
        module_exists = os.path.isfile(os.path.join(self.game_of_life_app_dir, 'models.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The game_of_life app's models.py module is missing.{FAILURE_FOOTER}")

    def test_is_game_of_life_app_configured(self):
        """
        Checks the new game_of_life app is added to the INSTALLED_APPS list
        """
        is_app_configured = 'game_of_life' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The game_of_life app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")
        

class InitialStateTests(TestCase):

    def test_default_state_creation(self):
        """
                Create a new state
        """
        u = User.objects.get_or_create(username = "TestName")[0]

        s = InitialState.objects.get_or_create(author = u)[0]
        s.name = 'TestState'
        s.state = [[0 for _ in range(100)]for _ in range(50)]
        s.save()

        self.assertEqual((s.author == u), True)
        self.assertEqual((s.name == 'TestState'), True)
        self.assertEqual((s.state == [[0 for _ in range(100)]for _ in range(50)]), True)
        self.assertEqual((s.views == 0), True)

    def like_increase(self):
        """
                Liking a state
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        s = InitialState.objects.get_or_create(author = u)[0]

        s.likes += 1
        s.save()

        self.assertEqual((s.likes == 0), True)

    def slug_check(self):
        """
                Check a state slug
        """
        u = User.objects.get_or_create(username = "Test Name")[0]
        s = InitialState.objects.get_or_create(author = u)[0]



        self.assertEqual((s.slug == slugify(self.name)), True)

    def no_name_duplicates(self):
        """
                No duplicate slug names allowed
        """

        u = User.objects.get_or_create(username = "TestName")[0]
        s = InitialState.objects.get_or_create(author = u)[0]

        d = InitialState.objects.get_or_create(author = u)[0]

        self.assertEqual(d, False)


class InterestingPattenTests(TestCase):

    def test_default_state_creation(self):
        """
                Create a new interesting pattern
        """

        s = InterestingPatten.objects.get_or_create(name = 'TestPattern')[0]
        s.state = [[0 for _ in range(100)]for _ in range(50)]
        s.save()

        self.assertEqual((s.name == 'TestPattern'), True)
        self.assertEqual((s.state == [[0 for _ in range(100)]for _ in range(50)]), True)

    def slug_check(self):
        """
                Check a state slug
        """
        s = InterestingPatten.objects.get_or_create(name = 'Test Pattern')[0]

        self.assertEqual((s.slug == slugify(self.name)), True)


class UserProfileTests(TestCase):

    def test_default_profile_creation(self):
        """
                Create a new profile
        """
        u = User.objects.get_or_create(username = "TestName")[0]

        p = UserProfile.objects.get_or_create(user = u)[0]
        p.save()

        self.assertEqual((p.user.username == 'TestName'), True)

    def test_adding_a_picture(self):
        """
                Adding a new profile pic
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        p = UserProfile.objects.get_or_create(user = u)[0]

        path = os.getcwd()
        path = os.path.join(path, "media")
        path = os.path.join(path, "test_profile_images")
        fullpath = os.path.join(path, "cat.jpg")

        p.picture = ImageFile(open(fullpath, "rb"))

        self.assertEqual((p.picture is not None), True)

    def test_picture_unique(self):
        """
                Adding a profile pic with the same name
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        p = UserProfile.objects.get_or_create(user = u)[0]

        u2 = User.objects.get_or_create(username = "TestName2")[0]
        p2 = UserProfile.objects.get_or_create(user = u2)[0]

        path = os.getcwd()
        path = os.path.join(path, "media")
        path = os.path.join(path, "test_profile_images")
        fullpath = os.path.join(path, "cat.jpg")

        p2.picture = ImageFile(open(fullpath, "rb"))

        self.assertEqual((p.picture != p2.picture), True)



    def test_adding_a_state(self):
        """
                Adding a state
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        p = UserProfile.objects.get_or_create(user = u)[0]
        s = InitialState.objects.get_or_create(author = u)[0]

        p.states += (s.state)

        self.assertEqual(s.state in p.states, True)


class FriendsListTests(TestCase):

    def test_regular_friends_list_creation(self):
        """
                Create a new FriendsList object
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        u.save()

        u_fl = FriendsList.objects.get_or_create(user=u)[0]
        u_fl.save()

        self.assertEqual(u_fl.user.username == "TestName", True)

    def adding_friend(self):
        """
               Adding a friend
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        u_fl = FriendsList.objects.get_or_create(user=u)[0]
        u_fl.friends.add(f)
        u_fl.save()

        self.assertEqual((f in u_fl.friends.all()), False)

    def removing_friend(self):
        """
               Removing a friend
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        u_fl = FriendsList.objects.get_or_create(user=u)[0]
        u_fl.friends.remove(f)
        u_fl.save()

        self.assertEqual((f in u_fl.friends.all()), False)


class LikedAndSavedTests(TestCase):

    def test_liked_and_saved_creation(self):
        """
                Create a new LikedAndSaved object
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        u.save()

        u_ls = LikedAndSaved.objects.get_or_create(user=u)[0]
        u_ls.save()

        self.assertEqual((u_ls.user.username == "TestName"), True)

    def test_like(self):

        """
                User like state
        """
        f = User.objects.get_or_create(username = "TestName2")[0]
        f.save()

        s = InitialState.objects.get_or_create(author = f)[0]
        s.name = 'TestState'
        s.state = [[0 for _ in range(100)]for _ in range(50)]
        s.save()

        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        s = InitialState.objects.get_or_create(author = f)[0]

        u_ls = LikedAndSaved.objects.get_or_create(user=u)[0]
        u_ls.liked.add(s)
        u_ls.save()

        self.assertEqual((s in u_ls.liked.all()), True)

    def test_save(self):

        """
                User save state
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        s = InitialState.objects.get_or_create(author = f)[0]

        u_ls = LikedAndSaved.objects.get_or_create(user=u)[0]
        u_ls.saved.add(s)
        u_ls.save()

        self.assertEqual((s in u_ls.saved.all()), True)

    def test_unlike(self):

        """
                User unlike state
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        s = InitialState.objects.get_or_create(author = f)[0]

        u_ls = LikedAndSaved.objects.get_or_create(user=u)[0]
        u_ls.liked.remove(s)
        u_ls.save()

        self.assertEqual((s in u_ls.liked.all()), False)

    def test_unsave(self):
        """
                User unsave state
        """
        u = User.objects.get_or_create(username = "TestName")[0]
        f = User.objects.get_or_create(username = "TestName2")[0]

        s = InitialState.objects.get_or_create(author = f)[0]

        u_ls = LikedAndSaved.objects.get_or_create(user=u)[0]
        u_ls.saved.remove(s)
        u_ls.save()

        self.assertEqual((s in u_ls.saved.all()), False)