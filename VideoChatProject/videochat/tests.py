from django.test import TestCase
from .models import Video
from django.test.client import RequestFactory

class VideoPlayMethodTest(TestCase):
	
	def _404_tests(self):

		request_factory = RequestFactory()
		url = 'http://localhost:8000/play/v/999999'
		request = request_factory.get(url)
		video_id = 999999 # Test: Video_id doesn't exist
		response = play(request, video_id)
		self.assertIs(video_id._404_tests,404)

	


