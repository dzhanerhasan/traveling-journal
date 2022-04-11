from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from finalProject.main.models import Picture, Album


class TestViews(TestCase):

    def setUp(self):

        self.client = Client()

        self.credentials = {
            'username': 'testuser',
            'password': 'aqwsaqws12'}

        self.user = User.objects.create_user(**self.credentials)
        self.album = Album.objects.create(author=self.user, title='Random')
        self.photo = Picture.objects.create(album=self.album,
                                            user=self.user,
                                            photo='default.jpg')

        self.client.login(**self.credentials)

        self.rq = RequestFactory()

    # Testing templates when user is logged out and logged in.

    def test_photo_create_view_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('create photo'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_photo_edit_view_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('edit photo', args=[self.photo.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_photo_delete_view_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('delete photo', args=[self.photo.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_photo_create_view_when_logged_in(self):
        response = self.client.get(reverse('create photo'))
        self.assertTemplateUsed(response, 'main/photo/create_photo.html')

    def test_photo_edit_view_when_logged_in(self):
        response = self.client.get(reverse('edit photo', args=[self.photo.pk]))
        self.assertTemplateUsed(response, 'main/photo/edit_photo.html')

    def test_photo_delete_view_when_logged_in(self):
        response = self.client.get(reverse('delete photo', args=[self.photo.pk]))
        self.assertTemplateUsed(response, 'main/photo/delete_photo.html')

    # Testing functionality of the views

    def test_create_photo_when_empty(self):
        response = self.client.post(reverse('create photo'))
        self.assertTemplateUsed(response, 'main/photo/create_photo.html')

    def test_create_photo_check_context(self):
        response = self.client.get(reverse('create photo'))
        album = response.context['album'].first()
        self.assertEquals(album, self.user.album_set.first())

    def test_delete_photo(self):
        response = self.client.post(reverse('delete photo', args=[self.photo.pk]))
        self.assertEquals(self.album.picture_set.count(), 0)

