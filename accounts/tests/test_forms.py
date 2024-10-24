from django.test import TestCase
from accounts import forms
from accounts.models import User

class TestUserRegisterForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            phone_number='09012345678',
            first_name='test',
            password='test_pass'
        )

    def test_valid_data(self):
        form = forms.UserRegisterForm(data={
            'phone_number': '09000000000',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = forms.UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_phone_number(self):
        form = forms.UserRegisterForm(data={
            'phone_number': '09012345678',
            'first_name': 'example',
            'password1': 'example_pass',
            'password2': 'example_pass',
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('phone_number'))

    def test_unmatch_password(self):
        form = forms.UserRegisterForm(data={
            'phone_number': '09000000000',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'example_pass',
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('password2'))

class TestUserCreationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            phone_number='09012345678',
            first_name='test',
            password='test_pass'
        )

    def test_valid_data(self):
        form = forms.UserCreationForm(data={
            'phone_number': '09000000000',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = forms.UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_phone_number(self):
        form = forms.UserCreationForm(data={
            'phone_number': '09012345678',
            'first_name': 'example',
            'password1': 'example_pass',
            'password2': 'example_pass',
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('phone_number'))

    def test_unmatch_password(self):
        form = forms.UserCreationForm(data={
            'phone_number': '09000000000',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'example_pass',
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('password2'))
