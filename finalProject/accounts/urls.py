from django.contrib.auth.views import LogoutView
from django.urls import path

from finalProject.accounts.views import LoginPage, RegistrationView, ProfileView, edit_profile, DeleteProfileView

urlpatterns = [
    path('login/', LoginPage.as_view(), name='log in'),
    path('logout/', LogoutView.as_view(next_page='log in'), name='log out'),
    path('register/', RegistrationView.as_view(), name='register'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit/', edit_profile, name='edit profile'),
    path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile')
]