from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, DeleteView

from finalProject.accounts.forms import RegistrationForm, EditProfileForm, EditUserForm


class LoginPage(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class RegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegistrationView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home page')
        return super(RegistrationView, self).get(*args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    context_object_name = 'user'
    model = User
    template_name = 'accounts/profile.html'


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit_profile.html', context)


class DeleteProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('log in')

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False
