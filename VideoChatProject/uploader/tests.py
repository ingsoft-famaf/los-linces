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

    def test_index_when_logged_in(self):
        response = self.client.get(reverse('uploader:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('uploader:index'))
