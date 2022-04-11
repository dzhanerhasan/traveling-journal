from django.urls import path

from finalProject.main.views.album import \
    AlbumCreateView, \
    AlbumEditView, \
    album_page, AlbumDeleteView, home_page

from finalProject.main.views.photos import PhotoCreateView, PhotoEditView, PhotoDeleteView

urlpatterns = [
    path('', home_page, name='home page'),

    path('create/', AlbumCreateView.as_view(), name='create album'),
    path('<int:pk>/', album_page, name='detail album'),
    path('edit/<int:pk>/', AlbumEditView.as_view(), name='edit album'),
    path('delete/<int:pk>/', AlbumDeleteView.as_view(), name='delete album'),

    path('photo/create/', PhotoCreateView.as_view(), name='create photo'),
    path('photo/edit/<int:pk>', PhotoEditView.as_view(), name='edit photo'),
    path('photo/delete/<int:pk>', PhotoDeleteView.as_view(), name='delete photo'),

]