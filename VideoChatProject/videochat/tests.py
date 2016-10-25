from django.test import TestCase
from .models import Video
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client

class VideoPlayMethodTest(TestCase):

	def setUp(self):
		self.video = Video(title= "Primer video", description= "probando", path="/media/videos/2016/10/20/sample4")
		self.video.save()
		self.videopk = self.video.pk
		self.client = Client()

	def test_404(self):

		request_factory = RequestFactory()
		#user = User.objects.create_user(username="pepita", password="contraseñadificil")
		#authenticate(username=user.username, password=user.password)
		self.videopk = self.video.pk + 1
		url = self.client.get(reverse('videochat: v'))
		request = request_factory.get(url)
		response = v(request, videopk)
		self.assertEqual(response.status_code,404)

	def _202_tests(self):
		
		request_factory = RequestFactory()
		url = 'http://localhost:8000/play/v/videopk'
		request = request_factory.get(url)
		self.videopk = self.video.pk
		#response = play(request, videopk)
		self.assertEqual(response.status_code,202)

	#def check_template_used():
		