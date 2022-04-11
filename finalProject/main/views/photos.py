from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from finalProject.main.forms import CreatePhotoForm, EditPhotoForm
from finalProject.main.models import Picture, Album


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Picture
    form_class = CreatePhotoForm
    template_name = 'main/photo/create_photo.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["album"] = user.album_set.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(PhotoCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picture
    form_class = EditPhotoForm
    template_name = 'main/photo/edit_photo.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PhotoEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        picture = self.get_object()
        if self.request.user == picture.user:
            return True
        return False


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = 'main/photo/delete_photo.html'

    def get_success_url(self):
        return reverse('detail album', kwargs={'pk': self.object.album.pk})

    def test_func(self):
        picture = self.get_object()
        if self.request.user == picture.user:
            return True
        return False
