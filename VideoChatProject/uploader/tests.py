from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class UserRedirectTest(TestCase):

    def test_index_redirect_when_not_logged_in(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertIs(response.status_code, 302)
        self.assertContains(response.url, 'login')
