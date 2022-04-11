from django.test import TestCase
from django.test import Client
from CoreApp.forms import *  # import all forms


class Profile_Form_Test(TestCase):

    # Valid Form Data
    def test_ProfileForm_valid(self):
        form = ProfileForm(data={'username': "user", 'first_name': "user", 'last_name': "user", 'email': "user@mp.com",
                                 'confirm_email': "user@mp.com"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_ProfileForm_invalid(self):
        form = ProfileForm(data={'username': "", 'first_name': "user", 'last_name': "user", 'email': ""})
        self.assertFalse(form.is_valid())


class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = UserForm(data={'username': "user", 'first_name': "user", 'last_name': "user", 'email': "user@mp.com"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = UserForm(data={'username': "", 'first_name': "user", 'last_name': "user", 'email': ""})
        self.assertFalse(form.is_valid())


class Post_Form_Test(TestCase):

    # Valid Form Data
    def test_PostForm_valid(self):
        form = PostForm(data={'content': "test"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_PostForm_invalid(self):
        form = PostForm(data={'content': ""})
        self.assertFalse(form.is_valid())


class Organizer_Form_Test(TestCase):

    # Valid Form Data
    def test_OrganizerForm_valid(self):
        form = OrganizerSignUpForm(data={'username': "user", 'password1': "123@django", 'password2': "123@django"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_OrganizerForm_invalid(self):
        form = OrganizerSignUpForm(data={'username': "", 'password1': "123@django", 'password2': ""})
        self.assertFalse(form.is_valid())


class Question_Form_Test(TestCase):

    # Valid Form Data
    def test_questionForm_valid(self):
        form = QuestionForm(data={'text': "dummy"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_questionForm_invalid(self):
        form = QuestionForm(data={'text': ""})
        self.assertFalse(form.is_valid())
