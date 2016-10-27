from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import setup_test_environment


class NonAuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_index_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('uploader:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/upload/')


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        username = "TestUser"
        password = "TestPassword"
        user = User.objects.create_user(username=username, password=password)
        user.save()
        self.client.login(username=username, password=password)
        self.THIS_FIELD_IS_REQUIRED = "This field is required"
        self.INVALID_FILE_EXTENSION = "Invalid file extension"


    def test_index_when_logged_in(self):
        response = self.client.get(reverse('uploader:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('uploader:index'))

    def test_upload_with_no_title(self):
        with open('manage.py') as fp:
            response = self.client.post(reverse('uploader:index'),
                {'description': "Description1", 'video_file': fp})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.THIS_FIELD_IS_REQUIRED)

    def test_upload_with_no_description(self):
        with open('manage.py') as fp:
            response = self.client.post(reverse('uploader:index'),
                {'title': "Title1", 'video_file': fp})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.THIS_FIELD_IS_REQUIRED)

    def test_upload_with_no_file(self):
        response = self.client.post(reverse('uploader:index'),
            {'title': "Title1", 'description': "Description1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.THIS_FIELD_IS_REQUIRED)

    def test_upload_with_wrong_file_extension(self):
        with open('manage.py') as fp:
            response = self.client.post(reverse('uploader:index'),
                {'title': "Title1",
                 'description': "Description1",
                 'video_file': fp})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.INVALID_FILE_EXTENSION)
