from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from finalProject.main.models import Album, Picture


# class HomePageView(LoginRequiredMixin, ListView):
#     model = Album
#     template_name = 'main/home.html'
#     context_object_name = 'albums'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['albums'] = context['albums'].filter(author=self.request.user)
#         return context

@login_required
def home_page(request):
    albums = Album.objects.filter(author=request.user)

    paginator = Paginator(albums, 9)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'albums': albums,
        'posts': posts,
    }

    return render(request, 'main/home.html', context)


@login_required
def album_page(request, pk):
    album_name = Album.objects.get(pk=pk)
    photos = Picture.objects.filter(album__pk=pk)
    current_user = None

    paginator = Paginator(photos, 6)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if photos:
        current_user = photos[0].album.author

        if request.user != current_user:
            return redirect('home page')

    context = {
        'album_name': album_name.title,
        'album_pk': pk,
        'photos': photos,
        'posts': posts,
    }

    return render(request, 'main/album/details_album.html', context)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'thumbnail']
    template_name = 'main/album/create_album.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = ['title', 'thumbnail']
    template_name = 'main/album/edit_album.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        album = self.get_object()
        if self.request.user == album.author:
            return True
        return False


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'main/album/delete_album.html'
    success_url = reverse_lazy('home page')

    def test_func(self):
        album = self.get_object()
        if self.request.user == album.author:
            return True
        return False
