from django.test import TestCase
from .models import Video
from django.test.client import RequestFactory
from django.contrib.auth.models import User

class VideoPlayMethodTest(TestCase):

	
	def _404_tests(self):

		request_factory = RequestFactory()
		#user = User.objects.create_user(username="pepita", password="contraseñadificil")
		#authenticate(username=user.username, password=user.password)
		video = Video(title= "Primer video", description= "probando", path="/media/videos/2016/10/20/sample4")
		video.save()
		videopk = video.pk + 1
		url = 'http://localhost:8000/play/v/videopk'
		request = request_factory.get(url)
		response = play(request, videopk)
		self.assertIs(videopk,404)

	