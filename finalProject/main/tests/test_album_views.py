from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from finalProject.main.models import Album


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'aqwsaqws12'}

        self.user = User.objects.create_user(**self.credentials)
        self.album = Album.objects.create(author=self.user, title='Random')
        self.client.login(**self.credentials)

    # Testing templates when logged in and logged out.

    def test_home_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('home page'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_home_page_when_logged_in(self):
        response = self.client.get(reverse('home page'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_album_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('detail album', args=[self.album.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_album_page_when_logged_in(self):
        response = self.client.get(reverse('detail album', args=[self.album.pk]))
        self.assertTemplateUsed(response, 'main/album/details_album.html')

    def test_album_create_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('create album'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_album_crate_page_when_logged_in(self):
        response = self.client.get(reverse('create album'))
        self.assertTemplateUsed(response, 'main/album/create_album.html')

    def test_album_edit_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('edit album', args=[self.album.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_album_edit_page_when_logged_in(self):
        response = self.client.get(reverse('edit album', args=[self.album.pk]))
        self.assertTemplateUsed(response, 'main/album/edit_album.html')

    def test_album_delete_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('delete album', args=[self.album.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_album_delete_page_when_logged_in(self):
        response = self.client.get(reverse('delete album', args=[self.album.pk]))
        self.assertTemplateUsed(response, 'main/album/delete_album.html')

    # Test functionality

    def test_home_page_correct_context(self):
        response = self.client.get(reverse('home page'))
        albums = response.context['albums'].first()
        self.assertEquals(albums, self.user.album_set.first())

    def test_album_page_correct_context(self):
        response = self.client.get(reverse('detail album', args=[self.album.pk]))
        photos = response.context['photos'].first()
        album_pk = response.context['album_pk']
        album_name = response.context['album_name']

        self.assertEquals(photos, self.album.picture_set.first())
        self.assertEquals(album_pk, self.album.pk)
        self.assertEquals(album_name, self.album.title)

    def test_album_create_when_successful(self):
        response = self.client.post(reverse('create album'),
                                    data={
                                        'title': 'testtitle',
                                    },
                                    follow=True
                                    )

        self.assertEquals(self.user.album_set.count(), 2)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_album_create_when_no_data(self):
        response = self.client.post(reverse('create album'), data={
        })

        self.assertEquals(self.user.album_set.count(), 1)
        self.assertTemplateUsed(response, 'main/album/create_album.html')

    def test_album_edit_when_successful(self):
        response = self.client.post(reverse('edit album', args=[self.album.pk]),
                                    data={
                                        'title': 'new_name',
                                    },
                                    follow=True
                                    )

        self.assertEquals(self.user.album_set.first().title, 'new_name')
        self.assertTemplateUsed(response, 'main/home.html')

    def test_album_edit_when_no_data(self):
        response = self.client.post(reverse('edit album', args=[self.album.pk]), data={
        })

        self.assertTemplateUsed(response, 'main/album/edit_album.html')

    def test_album_delete(self):
        response = self.client.post(reverse('delete album', args=[self.album.pk]),
                                    follow=True)

        self.assertEquals(self.user.album_set.count(), 0)
        self.assertTemplateUsed(response, 'main/home.html')

