from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'aqwsaqws12'}
        self.user = User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    # Testing templates when user is logged in and logged out.

    def test_login_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('log in'))
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_when_logged_in(self):
        response = self.client.get(reverse('log in'), follow=True)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_register_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_page_when_logged_in(self):
        response = self.client.get(reverse('register'), follow=True)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_profile_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('profile'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_profile_page_when_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_get_edit(self):
        response = self.client.get(reverse('edit profile'))
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_profile_get_edit_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('edit profile'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_profile_delete_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('delete profile', args=[self.user.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # Testing functionality

    def test_log_in_POST_with_correct_credentials(self):
        self.client.logout()
        response = self.client.post(reverse('log in'),
                                    {
                                        'username': 'testuser',
                                        'password': 'aqwsaqws12'
                                    },
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_log_in_POST_with_incorrect_credentials(self):
        self.client.logout()
        response = self.client.post(reverse('log in'),
                                    {
                                        'username': 'incorrect',
                                        'password': 'aqwsaqws12'
                                    },
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_register_POST_with_completed_requirements(self):
        self.client.logout()
        response = self.client.post(reverse('register'),
                                    {
                                        'username': 'testuser2',
                                        'email': 'test@email.com',
                                        'password1': 'aqwsaqws12',
                                        'password2': 'aqwsaqws12',
                                    },
                                    follow=True)

        self.assertEquals(User.objects.count(), 2)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_register_POST_with_incomplete_requirements(self):
        self.client.logout()
        response = self.client.post(reverse('register'),
                                    {
                                        'username': 'incorrect',
                                        'password1': 'aqwsaqws12'
                                    },
                                    )

        self.assertEquals(User.objects.count(), 1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_profile_edit_POST(self):
        response = self.client.post(reverse('edit profile'), {
            'username': 'new_username',
            'email': 'dzhanerrhasan@gmail.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')

    def test_profile_DELETE(self):
        response = self.client.delete(reverse('delete profile', args=[self.user.pk]))
        self.assertEquals(User.objects.count(), 0)

    def test_profile_page_context(self):
        response = self.client.get(reverse('profile'))
        profiles = response.context['user']
        self.assertEquals(profiles, self.user)