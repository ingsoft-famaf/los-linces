from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import setup_test_environment


class UploadTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/')
