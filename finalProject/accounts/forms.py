from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from finalProject.accounts.models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }


class EditUserForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  ]


class EditProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth',
                  'biography',
                  'gender',
                  'picture',
                  ]
