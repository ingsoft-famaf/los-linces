from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.files import File
from django.contrib.staticfiles import finders

'''
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
		url = self.client.get(reverse('videochat: play'))
		request = request_factory.get(url)
		response = v(request, videopk)
		self.assertEqual(response.status_code,404)

	def test_202(self):
		
		request_factory = RequestFactory()
		url = 'http://localhost:8000/play/v/videopk'
		request = request_factory.get(url)
		self.videopk = self.video.pk
		#response = play(request, videopk)
		self.assertEqual(response.status_code,202)

	#def check_template_used():
'''
class BaseTestCase(TestCase):

	def setUp(self):
		self.user_pw = 'test'
		self.user_turco = self.create_user('turco', 'turco@turco.com', self.user_pw)
		self.user_juampi = self.create_user('juampi', 'juampi@juampi.com', self.user_pw)
		self.user_male = self.create_user('male', 'male@male.com', self.user_pw)
		self.user_mono = self.create_user('mono', 'mono@mono.mono.com', self.user_pw)

	def tearDown(self):
		cache.clear()
		self.client.logout()

	def login(self, user, password):
		return login(self, user, password)

	def create_user(self, username, password, email_address):
		user = User.objects.create_user(username, password, email_address)
		return user

	def assertResponse200(self, response):
		self.assertEqual(response.status_code, 200)

	def assertResponse302(self, response):
	    self.assertEqual(response.status_code, 302)

	def assertResponse403(self, response):
	    self.assertEqual(response.status_code, 403)

	def assertResponse404(self, response):
		self.assertEqual(response.status_code, 404)


class FriendshipModelTest(BaseTestCase):

	def test_relationships(self):
		
		# Turco wants to be friends with Juampi
		req1 = Friend.objects.add_friend(self.user_turco, self.user_juampi)
		# Let's be sure they don't have any friends
		self.assertEqual(Friend.objects.friends(self.user_turco), [])
		self.assertEqual(Friend.objects.friends(self.user_juampi), [])
		'''
		Ensure they have the sent and received requests:
			Turco sent Juampi a request, so he should have 1 sent request and no received requests.
			Juampi should have Turco's sent request and no sent requests
		'''
		self.assertEqual(len(Friend.objects.requests(self.user_turco)), 0)
		self.assertEqual(len(Friend.objects.requests(self.user_juampi)), 1)
		self.assertEqual(len(Friend.objects.sent_requests(self.user_turco)), 1)
		self.assertEqual(len(Friend.objects.sent_requests(self.user_juampi)), 0)
		self.assertEqual(len(Friend.objects.unread_requests(self.user_juampi)), 1)
		self.assertEqual(Friend.objects.unread_request_count(self.user_juampi), 1)
		self.assertEqual(len(Friend.objects.rejected_requests(self.user_juampi)), 0)
		self.assertEqual(len(Friend.objects.unrejected_requests(self.user_juampi)), 1)
		self.assertEqual(Friend.objects.unrejected_request_count(self.user_juampi), 1)
		# Let's be sure they aren't friends at this point
		self.assertFalse(Friend.objects.are_friends(self.user_turco, self.user_juampi))
		# Accept the request
		req1.accept()
		# Ensure neither have pending requests
		self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_turco).count(), 0)
		self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_juampi).count(), 0)
		# Ensure both are in each other's friend lists
		self.assertEqual(Friend.objects.friends(self.user_turco), [self.user_juampi])
		self.assertEqual(Friend.objects.friends(self.user_juampi), [self.user_turco])
		self.assertTrue(Friend.objects.are_friends(self.user_turco, self.user_juampi))
		# Make sure we can remove friendship
		self.assertTrue(Friend.objects.remove_friend(self.user_turco, self.user_juampi))
		self.assertFalse(Friend.objects.are_friends(self.user_turco, self.user_juampi))
		self.assertFalse(Friend.objects.remove_friend(self.user_turco, self.user_juampi))
		# Male wants to be friends with Mono, but cancels it
		req2 = Friend.objects.add_friend(self.user_male, self.user_mono)
		self.assertEqual(Friend.objects.friends(self.user_male), [])
		self.assertEqual(Friend.objects.friends(self.user_mono), [])
		req2.cancel()
		self.assertEqual(Friend.objects.requests(self.user_male), [])
		self.assertEqual(Friend.objects.requests(self.user_mono), [])
		# Male wants to be friends with Mono, but Mono rejects it
		req3 = Friend.objects.add_friend(self.user_male, self.user_mono)
		self.assertEqual(Friend.objects.friends(self.user_male), [])
		self.assertEqual(Friend.objects.friends(self.user_mono), [])
		req3.reject()
		 # Duplicated requests raise a more specific subclass of IntegrityError.
		with self.assertRaises(AlreadyExistsError):
			Friend.objects.add_friend(self.user_male, self.user_mono)

		self.assertFalse(Friend.objects.are_friends(self.user_male, self.user_mono))
		self.assertEqual(len(Friend.objects.rejected_requests(self.user_mono)), 1)
		self.assertEqual(len(Friend.objects.rejected_requests(self.user_mono)), 1)

		# Let's try again...
		req3.delete()

		# Male wants to be friends with Mono, and Mono reads it
		req4 = Friend.objects.add_friend(self.user_male, self.user_mono)
		req4.mark_viewed()

		self.assertFalse(Friend.objects.are_friends(self.user_male, self.user_mono))
		self.assertEqual(len(Friend.objects.read_requests(self.user_mono)), 1)

		# Ensure we can't be friends with ourselves
		with self.assertRaises(ValidationError):
		    Friend.objects.add_friend(self.user_turco, self.user_turco)

		# Ensure we can't do it manually either
		with self.assertRaises(ValidationError):
			Friend.objects.create(to_user=self.user_turco, from_user=self.user_turco)

class VideoTest(BaseTestCase):
	
	def test_videoUpload(self):
		client = Client()
		# Log into a user's account
		response = client.post('/login/', {'username':'turco', 'password':self.user_pw})
		# Check if redirection happens
		self.assertResponse302(response)
		# Load testvideo from /static
		video = finders.find('static/testvideo.mp4')
		response = client.post('/upload/', {'title':'hola2', 'description':'caca', 'video_file':video})
		# Check if video was uploaded correctly
		self.assertResponse200(response)
