from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from finalProject.checklist.models import CheckList, ListItems


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'aqwsaqws12'}

        self.user = User.objects.create_user(**self.credentials)
        self.checklist = CheckList.objects.create(author=self.user, title='testlist')
        self.client.login(**self.credentials)

    # Testing templates when logged in and logged out.

    def test_checklists_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('home page'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_checklists_page_when_logged_in(self):
        response = self.client.get(reverse('checklist'))
        self.assertTemplateUsed(response, 'checklist/checklists.html')

    def test_checklist_details_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('detail album', args=[self.checklist.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_checklist_details_page_when_logged_in(self):
        response = self.client.get(reverse('details list', args=[self.checklist.pk]))
        self.assertTemplateUsed(response, 'checklist/checklist_page.html')

    def test_checklist_create_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('create list'), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_checklist_create_page_when_logged_in(self):
        response = self.client.get(reverse('create list'))
        self.assertTemplateUsed(response, 'checklist/create_checklist.html')

    def test_checklist_edit_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('edit list', args=[self.checklist.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_checklist_edit_page_when_logged_in(self):
        response = self.client.get(reverse('edit list', args=[self.checklist.pk]))
        self.assertTemplateUsed(response, 'checklist/edit_checklist.html')

    def test_checklist_delete_page_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('delete list', args=[self.checklist.pk]), follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_checklist_delete_page_when_logged_in(self):
        response = self.client.get(reverse('delete list', args=[self.checklist.pk]))
        self.assertTemplateUsed(response, 'checklist/delete_list.html')

    # Testing functionality

    def test_checklist_page_correct_context(self):
        response = self.client.get(reverse('checklist'))
        checklists = response.context['checklists'].first()
        self.assertEquals(checklists, self.user.checklist_set.first())

    def test_checklist_details_page_correct_context(self):
        response = self.client.get(reverse('details list', args=[self.checklist.pk]))
        plans = response.context['plans'].first()
        checklist_name = response.context['checklist_name']
        checklist_pk = response.context['checklist_pk']

        self.assertEquals(plans, self.checklist.listitems_set.first())
        self.assertEquals(checklist_name, self.checklist.title)
        self.assertEquals(checklist_pk, self.checklist.pk)

    def test_create_checklist_when_successful(self):
        response = self.client.post(reverse('create list'),
                                    data={
                                        'title': 'testtitle',
                                    },
                                    follow=True
                                    )

        self.assertEquals(self.user.checklist_set.count(), 2)
        self.assertTemplateUsed(response, 'checklist/checklists.html')

    def test_create_checklist_when_no_data(self):
        response = self.client.post(reverse('create list'), data={
        })

        self.assertEquals(self.user.checklist_set.count(), 1)
        self.assertTemplateUsed(response, 'checklist/create_checklist.html')

    def test_checklist_edit_when_successful(self):
        response = self.client.post(reverse('edit list', args=[self.checklist.pk]),
                                    data={
                                        'title': 'new_name',
                                    },
                                    follow=True
                                    )

        self.assertEquals(self.user.checklist_set.first().title, 'new_name')
        self.assertTemplateUsed(response, 'checklist/checklists.html')

    def test_checklist_edit_when_no_data(self):
        response = self.client.post(reverse('edit list', args=[self.checklist.pk]), data={
        })

        self.assertTemplateUsed(response, 'checklist/edit_checklist.html')

    def test_checklist_delete(self):
        response = self.client.post(reverse('delete list', args=[self.checklist.pk]),
                                    follow=True)

        self.assertEquals(self.user.album_set.count(), 0)
        self.assertTemplateUsed(response, 'checklist/checklists.html')

    def test_create_list_item_when_successful(self):
        response = self.client.post(reverse('details list', args=[self.checklist.pk]),
                                    data={'user': self.user,
                                          'checklist': self.checklist,
                                          'content': 'testtitle',
                                          },
                                    follow=True
                                    )

        self.assertEquals(self.checklist.listitems_set.count(), 1)
        self.assertTemplateUsed(response, 'checklist/checklist_page.html')

    def test_delete_list_item_when_successful(self):
        ListItems.objects.create(user=self.user,
                                 checklist=self.checklist,
                                 content='testtitle',
                                 )

        response = self.client.post(reverse('delete plan', args=[self.checklist.listitems_set.first().pk]),
                                    follow=True)

        self.assertEquals(self.checklist.listitems_set.count(), 0)
        self.assertTemplateUsed(response, 'checklist/checklist_page.html')
