from django.test import TestCase

from finalProject.accounts.forms import RegistrationForm, EditUserForm, EditProfileForm


class TestForms(TestCase):

    def test_registration_form(self):
        form = RegistrationForm(data={
            'username': 'dzhanerhasan',
            'email': 'dzhanerrhasan@gmail.com',
            'first_name': 'Dzhaner',
            'last_name': 'Hasan',
            'password1': 'aqwsaqws12',
            'password2': 'aqwsaqws12',
        })

        self.assertTrue(form.is_valid())

    def test_empty_registration_form(self):
        form = RegistrationForm(data={

        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_edit_user_form(self):
        form = EditUserForm(data={
            'username': 'dzhanerhasan',
            'email': 'dzhanerrhasan@gmail.com',
            'first_name': 'Dzhaner',
            'last_name': 'Hasan',
        })

        self.assertTrue(form.is_valid())

    def test_empty_edit_user_form(self):
        form = EditUserForm(data={

        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_edit_profile_form(self):
        form = EditProfileForm(data={
            'date_of_birth': '10/30/1998',
            'biography': 'Random bio',
            'gender': 'Male',
            'picture': 'default.jpg',
        })

        self.assertTrue(form.is_valid())

    def test_empty_edit_profile_form(self):
        form = EditProfileForm(data={

        })

        self.assertTrue(form.is_valid())
        self.assertEquals(len(form.errors), 0)
